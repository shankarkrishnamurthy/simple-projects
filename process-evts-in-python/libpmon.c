#include <sys/socket.h>
#include <linux/netlink.h>
#include <linux/connector.h>
#include <linux/cn_proc.h>
#include <sys/time.h>
#include <errno.h>
#include <stdbool.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <stdio.h>

static int dbg = 0;
static int nl_connect()
{
	int rc;
	int nl_sock;
	struct sockaddr_nl sa_nl;

	nl_sock = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_CONNECTOR);
	if (nl_sock == -1) {
		perror("socket");
		return -1;
	}

	sa_nl.nl_family = AF_NETLINK;
	sa_nl.nl_groups = CN_IDX_PROC;
	sa_nl.nl_pid = getpid();

	rc = bind(nl_sock, (struct sockaddr *)&sa_nl, sizeof(sa_nl));
	if (rc == -1) {
		perror("bind");
		close(nl_sock);
		return -1;
	}
	return nl_sock;
}

/*
* subscribe on proc events (process notifications)
*/
static int set_proc_ev_listen(int nl_sock, bool enable)
{
	int rc;
	struct __attribute__ ((aligned(NLMSG_ALIGNTO))) {
		struct nlmsghdr nl_hdr;
		struct __attribute__ ((__packed__)) {
			struct cn_msg cn_msg;
			enum proc_cn_mcast_op cn_mcast;
		};
	} nlcn_msg;

	memset(&nlcn_msg, 0, sizeof(nlcn_msg));
	nlcn_msg.nl_hdr.nlmsg_len = sizeof(nlcn_msg);
	nlcn_msg.nl_hdr.nlmsg_pid = getpid();
	nlcn_msg.nl_hdr.nlmsg_type = NLMSG_DONE;

	nlcn_msg.cn_msg.id.idx = CN_IDX_PROC;
	nlcn_msg.cn_msg.id.val = CN_VAL_PROC;
	nlcn_msg.cn_msg.len = sizeof(enum proc_cn_mcast_op);

	nlcn_msg.cn_mcast =
	    enable ? PROC_CN_MCAST_LISTEN : PROC_CN_MCAST_IGNORE;

	rc = send(nl_sock, &nlcn_msg, sizeof(nlcn_msg), 0);
	if (rc == -1) {
		perror("netlink send");
		return -1;
	}

	return 0;
}

typedef void (*cb_t) (int, void *);
static cb_t CB = NULL;

void register_cb(cb_t cb)
{
	CB = cb;
}

static volatile bool need_exit = false;
static int handle_proc_ev(int nl_sock)
{
	int rc;
	struct __attribute__ ((aligned(NLMSG_ALIGNTO))) {
		struct nlmsghdr nl_hdr;
		struct __attribute__ ((__packed__)) {
			struct cn_msg cn_msg;
			struct proc_event proc_ev;
		};
	} nlcn_msg;
	int buf[4];

	while (!need_exit) {
		rc = recv(nl_sock, &nlcn_msg, sizeof(nlcn_msg), 0);
		if (rc == 0) {
			/* shutdown? */
			return 0;
		} else if (rc == -1) {
			if (errno == EINTR) {
				continue;
			}
			perror("netlink recv");
			return -1;
		}

		switch (nlcn_msg.proc_ev.what) {
		case PROC_EVENT_NONE:
			if (dbg)
				printf("set mcast listen ok\n");
			buf[0] = buf[1] = buf[2] = buf[3] = -1;
			break;
		case PROC_EVENT_FORK:
			if (dbg)
				printf
				    ("fork(%d): parent tid=%d pid=%d -> child tid=%d pid=%d\n",
				     PROC_EVENT_FORK,
				     nlcn_msg.proc_ev.event_data.fork.
				     parent_pid,
				     nlcn_msg.proc_ev.event_data.fork.
				     parent_tgid,
				     nlcn_msg.proc_ev.event_data.fork.child_pid,
				     nlcn_msg.proc_ev.event_data.fork.
				     child_tgid);
			buf[0] = nlcn_msg.proc_ev.event_data.fork.parent_pid;
			buf[1] = nlcn_msg.proc_ev.event_data.fork.parent_tgid;
			buf[2] = nlcn_msg.proc_ev.event_data.fork.child_pid;
			buf[3] = nlcn_msg.proc_ev.event_data.fork.child_tgid;
			break;
		case PROC_EVENT_EXEC:
			if (dbg)
				printf("exec(%d): tid=%d pid=%d\n",
				       PROC_EVENT_EXEC,
				       nlcn_msg.proc_ev.event_data.exec.
				       process_pid,
				       nlcn_msg.proc_ev.event_data.exec.
				       process_tgid);
			buf[0] = nlcn_msg.proc_ev.event_data.exec.process_pid;
			buf[1] = nlcn_msg.proc_ev.event_data.exec.process_tgid;
			buf[2] = buf[3] = -1;
			break;
		case PROC_EVENT_UID:
			if (dbg)
				printf
				    ("uid change(%d): tid=%d pid=%d from %d to %d\n",
				     PROC_EVENT_UID,
				     nlcn_msg.proc_ev.event_data.id.process_pid,
				     nlcn_msg.proc_ev.event_data.id.
				     process_tgid,
				     nlcn_msg.proc_ev.event_data.id.r.ruid,
				     nlcn_msg.proc_ev.event_data.id.e.euid);
			buf[0] = nlcn_msg.proc_ev.event_data.id.process_pid;
			buf[1] = nlcn_msg.proc_ev.event_data.id.process_tgid;
			buf[2] = nlcn_msg.proc_ev.event_data.id.r.ruid;
			buf[3] = nlcn_msg.proc_ev.event_data.id.e.euid;
			break;
		case PROC_EVENT_GID:
			if (dbg)
				printf
				    ("gid change(%d): tid=%d pid=%d from %d to %d\n",
				     PROC_EVENT_GID,
				     nlcn_msg.proc_ev.event_data.id.process_pid,
				     nlcn_msg.proc_ev.event_data.id.
				     process_tgid,
				     nlcn_msg.proc_ev.event_data.id.r.rgid,
				     nlcn_msg.proc_ev.event_data.id.e.egid);
			buf[0] = nlcn_msg.proc_ev.event_data.id.process_pid;
			buf[1] = nlcn_msg.proc_ev.event_data.id.process_tgid;
			buf[2] = nlcn_msg.proc_ev.event_data.id.r.rgid;
			buf[3] = nlcn_msg.proc_ev.event_data.id.e.egid;
			break;
		case PROC_EVENT_EXIT:
			if (dbg)
				printf("exit(%d): tid=%d pid=%d exit_code=%d\n",
				       PROC_EVENT_EXIT,
				       nlcn_msg.proc_ev.event_data.exit.
				       process_pid,
				       nlcn_msg.proc_ev.event_data.exit.
				       process_tgid,
				       nlcn_msg.proc_ev.event_data.exit.
				       exit_code);
			buf[0] = nlcn_msg.proc_ev.event_data.exit.process_pid;
			buf[1] = nlcn_msg.proc_ev.event_data.exit.process_tgid;
			buf[2] = nlcn_msg.proc_ev.event_data.exit.exit_code;
			buf[3] = -1;
			break;
		default:
			if (dbg)
				printf("unhandled proc event (%d)\n",
				       nlcn_msg.proc_ev.what);
			buf[0] = buf[1] = buf[2] = buf[3] = -1;
			break;
		}

		// Execute CallBack (if present)

		if (CB) {
			if (dbg)
				printf("calling %d %p\n", nlcn_msg.proc_ev.what,
				       buf);
			(*CB) (nlcn_msg.proc_ev.what, buf);
		}
	}

	return 0;
}

void stop()
{
	kill(getpid(), SIGTERM);
	need_exit = true;
}

int handle()
{
	int nl_sock;
	int rc = EXIT_SUCCESS;

	nl_sock = nl_connect();
	if (nl_sock == -1)
		exit(EXIT_FAILURE);

	rc = set_proc_ev_listen(nl_sock, true);
	if (rc == -1) {
		rc = EXIT_FAILURE;
		goto out;
	}

	rc = handle_proc_ev(nl_sock);
	if (rc == -1) {
		rc = EXIT_FAILURE;
		goto out;
	}

	set_proc_ev_listen(nl_sock, false);

 out:
	close(nl_sock);
	return 0;
}

