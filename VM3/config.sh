# ce fichier est utilisé pour pouvoir lancer la configuration ansible directement au lancement de vagrant, voir le fichier vagrant associé
# changer la ligne suivante pour lancer les configs avec ou sans les améliorations..
echo m1reseaux | sudo -S ansible-playbook -c local -v /vagrant/config-with-amelioration-tun-radvd.yml