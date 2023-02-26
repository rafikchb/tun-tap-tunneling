#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/ioctl.h>

#include <unistd.h>
#include <fcntl.h>
#include <linux/if.h>
#include <linux/if_tun.h>


// les headers des fonctions
int tun_alloc(char *dev); 
void streamBetween(int src,int dest);

int tun_alloc(char *dev)
{
  struct ifreq ifr;
  int fd, err;

  if( (fd = open("/dev/net/tun", O_RDWR)) < 0 ){
    perror("alloc tun");
    exit(-1);
  }

  memset(&ifr, 0, sizeof(ifr));
  /* Flags: IFF_TUN   - TUN device (no Ethernet headers)
   *        IFF_TAP   - TAP device
   *
   *        IFF_NO_PI - Do not provide packet information
   */
   ifr.ifr_flags = IFF_TUN;
  if( *dev )
    strncpy(ifr.ifr_name, dev, IFNAMSIZ);

  if( (err = ioctl(fd, TUNSETIFF, (void *) &ifr)) < 0 ){
    close(fd);
    return err;
  }
  strcpy(dev, ifr.ifr_name);
  return fd;
}

void streamBetween(int src,int dest){
  // attention cette boucle est bloquante.
  // buffer utilisé pour stocker les données.
  // attention la taille doite être au moins égal a celle de la MTU de l'interface.
  char buff[1500];
  ssize_t nbrOfReadedBytes = 0; 
  while(1){
  nbrOfReadedBytes = read(src, buff ,sizeof(buff));
  if(nbrOfReadedBytes > 0)
  {
    write(dest , buff,nbrOfReadedBytes); 
    printf("\n"); 
  }
}
}
