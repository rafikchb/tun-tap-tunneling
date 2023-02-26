// TODO: revoire quelle sont les bibliotheque que l'lon doit garder .
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

// la bibliotheque iftun .
#include "./iftun/iftun.h" 
//////////////////////////

// utiliser la ligne suivante pour compiler directement dans le dossier de VM1
// gcc test_iftun.c -o ./../../VM1/test_iftun.c
int main (int argc, char** argv){
  int tunfd;
  printf("Création de %s\n",argv[1]);
  tunfd = tun_alloc(argv[1]);
  printf("Faire la configuration de %s...\n",argv[1]);
  printf("Appuyez sur une touche pour continuer\n");
  getchar();
  // instruction pour executer le fichier de configuration de de l'interface tun.
  system("cd /vagrant && bash configure-tun.sh");
  printf("Interface %s Configurée:\n",argv[1]);
  system("ip addr");
  // fonction utliser pour lire le descripteur de fichier associer a l'interface tun.
  streamBetween(tunfd , 1); 
  printf("Appuyez sur une touche pour terminer\n");
  getchar();
  return 0;
}
