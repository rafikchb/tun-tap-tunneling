# fichier de configuration de tun0 , 
# ce fichier doit etre commanter si le fichier de configuration ansible "config-with-amelioration-tun-radvd.yml" a etait utiliser 
ip -6 addr add fc00:1234:ffff::2/64 dev tun0
echo "l'adresse ip de tun0 a ete configurer sur fc00:1234:ffff::2/64"
ip link set up dev tun0
echo "l'interface tun0 a ete activer"
ip -6 route add fc00:1234:3::/64 via fc00:1234:ffff::1
ip -6 route list 