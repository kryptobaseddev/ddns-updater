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

- `DNS_PROVIDER`: Specify the DNS provider you're using (e.g., `namecheap`, `cloudflare`, etc.).
- `DOMAIN`: Your domain name.
- `SUBDOMAINS`: Comma-separated list of subdomains to update. Each subdomain should be specified without the domain name. For example, if you want to update `sub1.example.com` and `sub2.example.com`, you would set `SUBDOMAINS=sub1,sub2`.
- `PASSWORD`: Dynamic DNS password or API token for your DNS provider.
- `INTERVAL`: Interval for updating DNS records in seconds.

### Config.json

The `config.json` file contains configurations specific to the top common DNS providers. It includes the API URL and required fields for each provider. If you're using a provider not listed in the config.json file, you can manually specify the API URL and required fields in your `.env` file.

### Docker Compose

```bash
docker-compose build
docker-compose up
```

## Support

For any issues or questions, please [open an issue](https://github.com/kryptobaseddev/ddns-updater/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
