# Hydra config composition root
## Explains config groups and override patterns-

````markdown
# Configs

This directory contains the Hydra configuration files that define what dataset build should run.

The main entry point is `config.yaml`. It uses Hydra’s `defaults` list to compose a final runtime configuration from smaller reusable config groups, such as:

- `dataset/` — defines the dataset build recipe
- `source/` — defines where input data comes from
- `storage/` — defines where generated artifacts are written

For example:

```yaml
defaults:
  - dataset: demo
  - source: dummy
  - storage: local
  - _self_
````

This tells Hydra to compose:

```text
configs/dataset/demo.yaml
configs/source/dummy.yaml
configs/storage/local.yaml
```
