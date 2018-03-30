/*
 * Author: Shankar Krishanmurthy
 * Date: Dec 2013
 * Description:
 *      simple tap program (send and recv). Demo purpose only
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>        /* Must precede if*.h */
#include <linux/if.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/if_tun.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <errno.h>

union ethframe {
    struct {
        struct ethhdr header;
        unsigned char data[ETH_DATA_LEN];
    } field;
    unsigned char buffer[ETH_FRAME_LEN];
};
static char *iface = "tap1";    //source
static char *diface = "tap0";    //destination

static void get_index_from_intf(int s, char *iname, int *idx)
{
    struct ifreq buffer;
    memset(&buffer, 0x00, sizeof(buffer));
    strncpy(buffer.ifr_name, iname, IFNAMSIZ);
    if (ioctl(s, SIOCGIFINDEX, &buffer) < 0) {
        printf("Error: could not get interface %s index\n", iname);
        return;
    }
    *idx = buffer.ifr_ifindex;
    return;
}

static void get_hwadr_from_intf(int s, char *iname, char *ethaddr)
{
    struct ifreq buffer;
    memset(&buffer, 0x00, sizeof(buffer));
    strncpy(buffer.ifr_name, iname, IFNAMSIZ);
    if (ioctl(s, SIOCGIFHWADDR, &buffer) < 0) {
        printf("Error: could not get interface address %s\n", iname);
        return;
    }
    memcpy((void *)ethaddr, (void *)(buffer.ifr_hwaddr.sa_data), ETH_ALEN);
    return;
}

static void get_intf_up(int s, char *iname)
{
    struct ifreq buffer;
    memset(&buffer, 0x00, sizeof(buffer));
    strncpy(buffer.ifr_name, iname, IFNAMSIZ);
	if (ioctl(s, SIOCGIFFLAGS, &buffer) == -1) {
		perror("Could not get interface flags: %m");
	} else
        printf("flags %s = %#x ->", iname, buffer.ifr_flags);
    buffer.ifr_flags |= IFF_UP;
    if (ioctl(s, SIOCSIFFLAGS, &buffer) == -1) {
        perror("Could not set IFF_UP: %m");
	} else
        printf(" flags %#x succeeded\n", buffer.ifr_flags | IFF_UP);
}

int socket_side()
{
    unsigned char source[ETH_ALEN];
    unsigned char dest[ETH_ALEN];
    unsigned short proto = 0x1234;
    unsigned char *data = "Shankar experiment";
    unsigned short data_len = strlen(data);
    int s;
    int ifindex;
    int difindex;

    if ((s = socket(AF_PACKET, SOCK_RAW, htons(proto))) < 0) {
        printf("Error: could not open socket\n");
        return -1;
    }

    get_index_from_intf(s, iface, &ifindex);
    printf("Interface %s index %d\n", iface, ifindex);
    get_index_from_intf(s, diface, &difindex);
    printf("Interface %s index %d\n", diface, ifindex);

    get_hwadr_from_intf(s, iface, source);
    printf("Source (%s) MAC %x:%x:%x:%x:%x:%x\n", iface, source[0],
           source[1], source[2], source[3], source[4], source[5]);
    get_hwadr_from_intf(s, diface, dest);
    printf("Dest (%s) MAC %x:%x:%x:%x:%x:%x\n", diface, dest[0], dest[1],
           dest[2], dest[3], dest[4], dest[5]);

    /* 
       socket sendto call will not succeed (neither do tcpdump)
       without the interface being 'up'
     */
    get_intf_up(s, iface);
    get_intf_up(s, diface);

    /* Form an ethernet Frame */
    union ethframe frame;
    memcpy(frame.field.header.h_dest, dest, ETH_ALEN);
    memcpy(frame.field.header.h_source, source, ETH_ALEN);
    frame.field.header.h_proto = htons(proto);
    memcpy(frame.field.data, data, data_len);
    unsigned int frame_len = data_len + ETH_HLEN;

    struct sockaddr_ll saddrll;
    memset((void *)&saddrll, 0, sizeof(saddrll));
    saddrll.sll_family = PF_PACKET;
    saddrll.sll_halen = ETH_ALEN;
    saddrll.sll_ifindex = difindex;
    memcpy((void *)(saddrll.sll_addr), (void *)dest, ETH_ALEN);

    /* Send the frame to tap interface through socket layer */
    if ((frame_len = sendto(s, frame.buffer, frame_len, 0,
                (struct sockaddr *)&saddrll,
                sizeof(saddrll))) > 0)
        printf("SEND Success ! %d\n", frame_len);
    else
        printf("Error, could not send\n");

    struct sockaddr_ll saddrll_receive;
    memset((void *)&saddrll_receive, 0, sizeof(saddrll_receive));
    socklen_t sll_len = (socklen_t) sizeof(saddrll_receive);

    int recv_result;
    char buffer_receive[ETH_FRAME_LEN];
    //saddrll.sll_ifindex = ifindex;
    //memcpy((void *)(saddrll.sll_addr), (void *)source, ETH_ALEN);
    recv_result = recvfrom(s, buffer_receive, frame_len, 0, NULL, NULL);

    if (recv_result > 0)
        printf("RECV bytes %d (from tap1) data: \"%s\"\n", recv_result,
               buffer_receive + ETH_HLEN);
    else
        printf("Error, could not receive\n");

    close(s);

    return 0;
}

int tun_alloc(char *dev, int flags)
{

    struct ifreq ifr;
    int fd, err;

    if ((fd = open("/dev/net/tun", O_RDWR)) < 0) {
        perror("Opening /dev/net/tun");
        return fd;
    }

    memset(&ifr, 0, sizeof(ifr));

    ifr.ifr_flags = flags;

    if (*dev) {
        strncpy(ifr.ifr_name, dev, IFNAMSIZ);
    }

    if ((err = ioctl(fd, TUNSETIFF, (void *)&ifr)) < 0) {
        perror("ioctl(TUNSETIFF)");
        close(fd);
        return err;
    }

    return fd;
}

int cread(int fd, char *buf, int n)
{
    int nread;
    if ((nread = read(fd, buf, n)) < 0) {
        perror("Reading data");
    }
    return nread;
}

void tap_side()
{
    int tap0_fd, tap1_fd;
    int maxfd;
    /* initialize tun/tap interface */
    if ((tap0_fd = tun_alloc(diface, IFF_TAP | IFF_NO_PI)) < 0) {
        fprintf(stderr, "Error connecting to tun/tap interface %s!\n",
            diface);
        return;
    }
    if ((tap1_fd = tun_alloc(iface, IFF_TAP | IFF_NO_PI)) < 0) {
        fprintf(stderr, "Error connecting to tun/tap interface %s!\n",
            iface);
        return;
    }
    printf("tap0_fd = %d tap2_fd = %d\n", tap0_fd, tap1_fd);

    maxfd = (tap0_fd > tap1_fd) ? tap0_fd : tap1_fd;
    while (1) {
        int ret;
        fd_set rd_set;
        char buf[128];

        FD_ZERO(&rd_set);
        FD_SET(tap0_fd, &rd_set);
        FD_SET(tap1_fd, &rd_set);

        ret = select(maxfd + 1, &rd_set, NULL, NULL, NULL);

        if (ret < 0 && errno == EINTR) {
            continue;
        }

        if (ret < 0) {
            perror("select()");
        }

        if (FD_ISSET(tap0_fd, &rd_set)) {
            printf("*GOT tap0 fd set\n");

            /*  
               The TX that got started from parent thread 
               sendto() fn eventually calls ->dev_hard_start_xmit()
               which will not complete unless we read from tap0 fd.
               Reading from tap0 FD causes call tun_aio_read()->
               tun_put_user() which increments the tx pkt stat of tap0
             */
            memset(buf, 0, 128);
            int bytes = cread(tap0_fd, buf, 1024);
            printf("READ %d bytes (from tap0) data: \"%s\"\n",
                   bytes, buf + ETH_HLEN);

            /*      
               The recvfrom() socket call on the tap1 will not complete
               unless a ethernet frame ends up in RX of tap1. This can
               be achieved strangely by 'write' syscall on the tap1.
               The act of write will increment the rx pkt stat on tap1
               (and recvfrom will merely give it to user)
             */

            /* Lets write() slightly modifed string into tap1 fd */
            char *ptr = buf + ETH_HLEN;
            strncpy(ptr, "Bharath", 7);
            ret = write(tap1_fd, buf, bytes);
            printf
                ("written %d bytes (modified from tap0) into tap1\n",
                 ret);
            break;
        }
        if (FD_ISSET(tap1_fd, &rd_set)) {
            printf("*GOT tap0 fd set\n");
        }
    }
}

int main(int argc, char *argv[])
{
    if (fork()) { 
        // This ensures that tap devices (tap0 & tap1)
        // are created before we perform socket operation.
        sleep(1);
        /* parent */
        socket_side();
    } else {
        /* Child */
        tap_side();
    }
    return 0;
}
