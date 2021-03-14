statx() {
  for file in "${@}"; do
    fs=$(df "${file}"  | tail -1 | awk '{print $1}')
    #echo sudo debugfs -R 'stat '"${file}" "${fs}"
    crtime=$(sudo debugfs -R 'stat '"${file}" "${fs}" 2>/dev/null | 
    grep -oP 'crtime.*--\s*\K.*')
    printf "%s\t%s\n" "${crtime}" "${file}"
  done
}
statx "$*"
