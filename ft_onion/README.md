# ft_onion

## Docker Project Architecture

- Your PC (host)
  - Docker Container (server)
    - Nginx (web server)
      - Serves the static site "index.html"
      - Listens on port 80
    - Tor (anonymization service)
      - Redirects .onion requests to Nginx
      - Uses default Tor port 9050 for internal communication
    - SSH (sshd)
      - Allows remote connection for administration that can be root
      - Listens on port 4242
      - Provides a terminal session inside the container


## What is a `.onion` Address?

- A `.onion` address is a **hidden service** accessible **only through the Tor network**.  
- It is generated from a public/private key pair and does **not exist on the regular Internet**. 

---

## The Link Between Tor and `.onion

- **Tor is required** to create and access a `.onion` service.  
- Without Tor, a browser **cannot resolve a `.onion` address**.
- Tor provides:
  - **Anonymous routing** of requests
  - **IP protection** for both server and clients  
  - **End-to-end encryption** between the client and the hidden service  

> In short: `.onion` = a web service hosted on Tor (Tor makes the address reachable and anonymous)

---

## Difference Between `.onion` and Regular Websites

| Feature                 | Regular Web                   | .onion (Tor Hidden Service) |
|-------------------------|-------------------------------|-----------------------------|
| DNS Resolution          | Standard DNS                  | No, only resolvable via Tor |
| Access                  | Chrome / Firefox / Edge       | Tor Browser or Tor client   |
| Visibility              | Indexed by search engines     | Not publicly indexed        |
| IP Exposure             | Can reveal server IP          | Server IP hidden via Tor    |

---

## Configure tor in your docker

#### In torrc
`HiddenServicePort 80 127.0.0.1:80` means: `HiddenServicePort <hidden-service-port> <target-address>:<target-port>`


- The Tor hidden service will listen on **port 80** for `.onion` requests.
- Any request received by Tor on this hidden service port is **forwarded to `127.0.0.1:80`**, which is where **Nginx** is running inside the container.
- Essentially, Tor acts as a **bridge** between the Tor network and your local web server.

This makes it clear that Tor doesn’t serve the page itself—it just redirects traffic to Nginx.

# Usage

## Start the services (Tor and Nginx)
```bash
make up
```

## How to Access a `.onion` Site

1. Install [Tor Browser](https://www.torproject.org).  
2. Obtain the `.onion` address (from Tor’s `hostname` file in your Hidden Service directory).  
3. Enter the address in Tor Browser to access the site.  

### Get the .onion address
```
docker exec -it tor cat /var/lib/tor/hidden_service/hostname
-> xxxx.onion
```

You must know use Tor Browser to access the .onion address.
Then copy paste the xxxx.onion adress

---

# sshd sever

## How to know if the ssh connection is mapped with 4242 port of the machine

```bash
~ docker port onion
80/tcp -> 0.0.0.0:8080
80/tcp -> [::]:8080
4242/tcp -> 0.0.0.0:4342
4242/tcp -> [::]:4342
```
