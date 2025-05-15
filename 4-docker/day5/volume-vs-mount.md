# Docker Volume vs Mount Options

The `--volume` and `--mount` flags in Docker both provide ways to persist data and share it between containers, but they have some key differences:

## Volume (`--volume` or `-v`)

- **Older syntax**: The original method for managing volumes
- **Format**: `-v [source]:[destination]:[options]`
- **Behavior**: Creates the host directory if it doesn't exist
- **Error checking**: Less strict validation
- **Simplicity**: More concise syntax

## Mount (`--mount`)

- **Newer syntax**: Introduced in Docker 17.06
- **Format**: `--mount type=bind,source=[source],target=[destination],readonly`
- **Behavior**: Requires the host directory to exist before mounting
- **Error checking**: More explicit error messages and validation
- **Consistency**: Same syntax across different mount types (volume, bind, tmpfs)
- **Flexibility**: Supports more options with explicit key-value pairs

## Example Comparison

**Using volume:**

```
docker run -v /host/path:/container/path:ro my-image
```

**Using mount:**

```
docker run --mount type=bind,source=/host/path,target=/container/path,readonly my-image
```

Docker recommends using `--mount` for Docker services and in newer applications as it's more explicit and offers better error messaging. However, the `-v` syntax remains popular for its brevity, especially in quick commands and legacy scripts.

# Docker `--mount` Flag Properties

The `--mount` flag offers a more explicit and versatile approach to mounting data in Docker containers. Here's a comprehensive list of the properties you can use:

## Core Properties

| Property                           | Description                                         | Required?                                   |
| ---------------------------------- | --------------------------------------------------- | ------------------------------------------- |
| `type`                             | Mount type: `bind`, `volume`, or `tmpfs`            | Yes                                         |
| `source` or `src`                  | Source for the mount (volume name, host path, etc.) | Yes for `bind` and `volume`, No for `tmpfs` |
| `target` or `dst` or `destination` | Mount point within the container                    | Yes                                         |

## Common Options

| Property           | Description                                                                                        | Default      |
| ------------------ | -------------------------------------------------------------------------------------------------- | ------------ |
| `readonly` or `ro` | Makes the mount read-only                                                                          | `false`      |
| `consistency`      | Consistency requirements (for macOS): `consistent`, `cached`, or `delegated`                       | OS dependent |
| `bind-propagation` | Propagation mode for bind mounts: `private`, `rprivate`, `shared`, `rshared`, `slave`, or `rslave` | `rprivate`   |

## Volume-Specific Options

| Property        | Description                                                     |
| --------------- | --------------------------------------------------------------- |
| `volume-label`  | Custom metadata for the volume                                  |
| `volume-opt`    | Volume driver-specific options                                  |
| `volume-nocopy` | Disables copying data from a container when a volume is created |

## Bind-Specific Options

| Property            | Description                                   |
| ------------------- | --------------------------------------------- |
| `bind-nonrecursive` | Disables recursive propagation of bind mounts |

## Tmpfs-Specific Options

| Property     | Description                                             |
| ------------ | ------------------------------------------------------- |
| `tmpfs-size` | Size of the tmpfs mount in bytes (e.g., `1000000`)      |
| `tmpfs-mode` | File mode of the tmpfs in octal (e.g., `700` or `0700`) |

## Examples

**Volume mount:**

```
docker run --mount type=volume,source=my-vol,target=/app/data,readonly my-image
```

**Bind mount:**

```
docker run --mount type=bind,source=/host/logs,target=/container/logs,bind-propagation=rslave my-image
```

**Tmpfs mount:**

```
docker run --mount type=tmpfs,target=/app/temp,tmpfs-size=100000000 my-image
```

**Multiple options:**

```
docker run --mount type=bind,source=/configs,target=/etc/configs,readonly,bind-propagation=shared my-image
```

The explicit key-value format of `--mount` makes these options clearer and less error-prone than the more compact `-v` syntax, especially when you need to use multiple mount options.
