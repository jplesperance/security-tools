go build -o server main.go
echo "Sudo for cap net bind"
sudo setcap 'cap_net_bind_service=+3p' ./server
