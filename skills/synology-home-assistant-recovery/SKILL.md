---
name: synology-home-assistant-recovery
description: Diagnose and recover Home Assistant containers on Synology NAS when the web UI or port 8123 is unavailable, including Docker restart recovery when requested.
---

# Synology Home Assistant Recovery

Use this skill when Home Assistant is hosted in Synology Container Manager and its UI or network connection is unavailable.

## Connect safely

- Use the NAS hostname or IP and SSH alias supplied by the user or already configured on the machine. Do not guess a host, username, or key path.
- Prefer the existing SSH agent or SSH config. Never print, copy, or save private key contents. Do not include machine-specific addresses, usernames, aliases, or key paths in this skill or other shared files.
- On DSM, the Container Manager Docker CLI is commonly at `/var/packages/ContainerManager/target/usr/bin/docker`; confirm the path on the target before using it.

## Diagnose

1. Begin with read-only checks: SSH reachability, Home Assistant container state, restart policy, network mode, port listener, and HTTP response from the NAS itself.
2. Identify the container from `docker ps -a` and its image or Compose labels. Do not assume a name if the host has multiple Home Assistant containers.
3. Use `docker inspect` to check status, exit code, OOM state, restart policy, network mode, and port bindings. With host networking, no Docker port binding is needed; Home Assistant should listen on port `8123` on the NAS. With bridge networking, verify the NAS port is published to container port `8123`.
4. Distinguish name resolution failures from refused connections. A DNS failure means the hostname did not resolve; a refused connection means the target was reached but nothing accepted that port.
5. Check the listener with `ss -lnt` or `netstat -lnt`, and make a bounded HTTP request to `http://127.0.0.1:8123/` from the NAS. If local access works but LAN access fails, check the bind address, port publishing, and network/firewall path.
6. Inspect only targeted recent logs. Do not dump environment variables or full configuration. Redact tokens, passwords, API keys, authorization values, and device identifiers before reporting.

## Recover

- Starting Home Assistant can resume automations and reconnect to devices. Start it only when the user asks to restore service or otherwise authorizes that action.
- Start the existing container without recreating it or changing its configuration:

  ```sh
  <docker-cli> start <home-assistant-container>
  ```

- When the user requests recovery after NAS restarts or container exits, configure the existing container to restart unless an operator has explicitly stopped it:

  ```sh
  <docker-cli> update --restart unless-stopped <home-assistant-container>
  ```

- `unless-stopped` starts the container with Docker after NAS startup and retries after container exit. It does not repair a bad configuration, host failure, or a process that remains running but unhealthy.
- Do not recreate the container, alter its network, ports, volumes, or firewall rules unless the user specifically requests that repair.

## Verify and report

After a recovery action, verify the intended container is running, the requested restart policy is set, and port `8123` is listening. Confirm an HTTP response from the NAS and, when possible, test `http://<NAS-IP>:8123` from a browser on the user's network. Report the observed cause, exact changes, and any checks that remain incomplete.
