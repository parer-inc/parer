# parer
Youtube parser\
Installation script:

```console
mkdir -p parer-inc;
cd parer-inc;
curl -s https://api.github.com/orgs/parer-inc/repos | grep -e 'clone_url*' | cut -d \" -f 4 | xargs -L1 git clone
```
