# MyLife Tracker — Home Assistant integration

HACS custom integration for the self-hosted **MyLife Tracker** app. Polls `/api/ha/status` and exposes sensors, binary sensors, and buttons for dashboards and automations.

Pair with the **[MyLife Tracker Card](https://github.com/benalfoldi/mylife-tracker-card)** Lovelace plugin for a dashboard card.

## Features

- **Sensors** — badge counts, unpaid bill/extra-cost counts, document expiry counts
- **Status sensor** — master entity with full lists in attributes (`unpaid_bills`, `warning_docs`, …)
- **Binary sensors** — `has_unpaid_bills`, `has_unpaid_extra_costs`, `has_expired_docs`, `has_warning_docs`
- **Buttons** — refresh status, trigger server-side webhook push
- **Service** — `mylife_tracker.refresh`

## Requirements

- Home Assistant 2023.8+
- A self-hosted MyLife Tracker instance with the HA API enabled (`HA_API_KEY` in server `.env`)
- Network access from Home Assistant to your server URL

## Install via HACS

1. **HACS → Integrations → ⋮ → Custom repositories**
2. URL: `https://github.com/benalfoldi/mylife-tracker-home-assistant`
3. Category: **Integration** → **Add**
4. Search **MyLife Tracker** → **Download**
5. Restart Home Assistant

## Configure

**Settings → Devices & services → Add integration → MyLife Tracker**

| Field | Description |
|-------|-------------|
| **Server URL** | Base URL of *your* MyLife Tracker server (e.g. `https://mylife.example.com`) |
| **API key** | The `HA_API_KEY` value from your server's `.env` |
| **Poll interval** | Seconds between polls (default 300, minimum 60) |

Credentials and URL are stored only in your Home Assistant config — nothing is sent to GitHub or third parties.

## Entities

| Entity | Type | Description |
|--------|------|-------------|
| Status | sensor | Total badge count; attributes hold full lists |
| Badge / documents / payments counts | sensor | Numeric badges |
| Unpaid bills / extra costs | sensor + binary_sensor | Count and on/off |
| Expired / warning documents | sensor + binary_sensor | Count and on/off |
| Refresh status | button | Poll API now |
| Push to webhook | button | Calls `POST /api/ha/push` on your server |

Entity IDs look like `sensor.mylife_tracker_status`.

## Dashboard card

```yaml
type: custom:mylife-tracker-card
entity: sensor.mylife_tracker_status
theme: brand
min_year: 2025
```

Install the card from [mylife-tracker-card](https://github.com/benalfoldi/mylife-tracker-card).

## Automations

```yaml
alias: MyLife unpaid bills
trigger:
  - platform: state
    entity_id: binary_sensor.mylife_tracker_has_unpaid_bills
    to: "on"
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "Unpaid bills"
      message: "{{ states('sensor.mylife_tracker_unpaid_bills') }} due"
```

## Webhook push (optional)

On your MyLife Tracker server, set `HA_WEBHOOK_URL` to your Home Assistant webhook URL. The integration still polls as backup.

## Service

```yaml
service: mylife_tracker.refresh
```

## Development

Copy `custom_components/mylife_tracker` into `config/custom_components/` and restart Home Assistant.
