# View Change Record and Incident Details

## Description
The `view-change-record` command is used to query ServiceNow to retrieve a summary of an MCR or an Incident.

!!! info "Assignment Group"
    The CLI can only display information on MCRs linked to the **HBO Change** assignment group.

## Usage

```sh
s3-cli view-change-record --number <ChangeRecord>
```

## Arguments

- `--number`: The change record or incident number you want to view.

## Example

```bash
$ s3-cli view-change-record --number INC000000

2024-12-05 11:35:28,963 [INFO] CLI running with profile: default
2024-12-05 11:35:28,973 [INFO] Validating change record: INC000000
                               Displaying Change Record: INC000000  
┏━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ valid ┃ number    ┃ short_description                    ┃ assignment_group                       ┃ description                             ┃ state ┃ start_date ┃ end_date ┃ invalid_reason ┃
┡━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ True  │ INC000000 │ Request CA00296640 out of agreed SLA │ {'link':                               │ Request CA00296640 out of agreed SLA.   │ 7     │ N/A        │ N/A      │ N/A            │
│       │           │                                      │ HttpUrl('https://rbs.service-now.com/… │ This request has been chased via Ask    │       │            │          │                │
│       │           │                                      │ 'value':                               │ Archie...                               │       │            │          │                │
│       │           │                                      │ '4f9a5f930fa6d680dcc74ebce1050eb9'}    │                                         │       │            │          │                │
└───────┴───────────┴──────────────────────────────────────┴────────────────────────────────────────┴─────────────────────────────────────────┴───────┴────────────┴──────────┴────────────────┘

```
