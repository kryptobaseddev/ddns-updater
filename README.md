# Dynamic DNS Updater

Automatically update DNS records based on your dynamic IP address.

## Overview

This Python script runs as a Docker container, updating your DNS records with your current IP address. It supports various DNS providers such as Namecheap, Cloudflare, Google Domains, and more.

## Features

- **Dynamic Updates**: Automatically updates DNS records based on your current public IP address.
- **Multiple Providers**: Supports popular DNS providers like Namecheap, Cloudflare, Google Domains, and more.
- **Configurability**: Customize settings via environment variables or a configuration file.
- **Interval Updates**: Set intervals for automatic updates to suit your needs.

## Getting Started

1. Clone this repository to your local machine.
2. Copy the `.env.sample` to `.env` file and set up your environment variables.
3. Build the Docker image using `docker-compose build`.
4. Run the Docker container using `docker-compose up`.

## Usage

### Environment Variables

Before running the container, you need to set up the following environment variables:

| Variable Name | Default Value | Description                                          |
|---------------|---------------|------------------------------------------------------|
| DNS_PROVIDER  |  <required>   | Choose a DNS provider from the supported list below. |
| DOMAIN        |  <required>   | Your domain name (e.g., `mydomain.com`).             |
| SUBDOMAINS    |  <required>   | Comma-separated list of subdomains.                  |
| PASSWORD      |  <required>   | The DDNS or API pass key provided by your DNS provider. |
| INTERVAL      | 3600          | The amount of time to wait until the next IP check and update in seconds. |

### Config.json

The `config.json` file contains configurations specific to the top common DNS providers. It includes the API URL and required fields for each provider. If you're using a provider not listed in the config.json file, you can manually specify the API URL and required fields in your `.env` file.

### Docker Compose

```bash
docker-compose build
docker-compose up
```

## Support

For any issues or questions, please [open an issue](https://github.com/yourusername/your-repo/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The Docker Hub overview file has been updated as follows:

**Dynamic DNS Updater**

This Docker image provides a lightweight solution for dynamically updating DNS records using various DNS providers. It can be used to automatically update the IP address of your domain's A records based on your current public IP address.

**Features:**
- Supports multiple DNS providers, including Namecheap, Cloudflare, Google Domains, and more.
- Configurable via environment variables for easy customization.
- Automatically updates DNS records at specified intervals.
- Compatible with any DNS provider that supports dynamic DNS updates.

**Usage:**

1. **Setting up Environment Variables:**

   Before running the container, you need to set up the following environment variables:

| Variable Name | Default Value | Description                                          |
|---------------|---------------|------------------------------------------------------|
| DNS_PROVIDER  |  <required>   | Choose a DNS provider from the supported list below. |
| DOMAIN        |  <required>   | Your domain name (e.g., `mydomain.com`).             |
| SUBDOMAINS    |  <required>   | Comma-separated list of subdomains.                  |
| PASSWORD      |  <required>   | The DDNS or API pass key provided by your DNS provider. |
| INTERVAL      | 3600s         | The amount of time to wait until the next IP check and update in seconds. |

2. **Running the Container via Docker Compose:**

   - Copy teh `.env.sample` to `.env` file in the root directory of your project.
   - Set the environment variables in the `.env` file according to the instructions above.
   - Run the Docker container using `docker-compose up`.

3. **Running the Container via Synology Container Manager (Docker):**

   - In Synology Container Manager, search for `kryptobaseddev/ddns-updater` and download it.
   - Run the container and name it accordingly.
   - Enable auto-restart and click next
   - In the Environment section add the following variables:
       - `DNS_PROVIDER`: Choose a DNS provider from the supported list below.
       - `DOMAIN`: Your domain name (e.g., `mydomain.com`).
       - `SUBDOMAINS`: Comma-separated list of subdomains.
       - `PASSWORD`: The DDNS or API pass key provided by your DNS provider.
       - `INTERVAL`: The amount of time to wait until the next IP check and update in seconds.
   - Under Network, select `bridge` and click next.
   - Validate the settings, chekcing `Run this container...` and click `Done` to start the container.

For detailed usage instructions, configuration options, and supported DNS providers, please refer to the [GitHub repository](https://github.com/kryptobaseddev/ddns-updater).

**Supported DNS Providers:**

| Provider Name | Variable Name | Required Fields                        |
|---------------|---------------|----------------------------------------|
| Namecheap     | DNS_PROVIDER  | domain, password, subdomains           |
| Cloudflare    | DNS_PROVIDER  | zone_id, api_token, subdomains         |
| Google        | DNS_PROVIDER  | domain, password                       |
| AWS           | DNS_PROVIDER  | access_key, secret_key, zone_id, subdomains |
| DigitalOcean  | DNS_PROVIDER  | token, domain, subdomains              |
| Linode        | DNS_PROVIDER  | token, domain, subdomains              |
| CloudNS       | DNS_PROVIDER  | auth_id, password, domain              |
| DuckDNS       | DNS_PROVIDER  | domain, token                          |
| DynDNS        | DNS_PROVIDER  | hostname, username, password           |
| FreeDNS       | DNS_PROVIDER  | hostname, password                     |
| No-IP         | DNS_PROVIDER  | hostname, username, password           |
| nsupdate      | DNS_PROVIDER  | hostname, key                          |

**Note:** This image assumes familiarity with Docker and basic DNS management concepts. It is recommended for users who need a simple and automated solution for updating DNS records.
