Needs a secret in kubernetes with name: `datasafe-keys`, which holds "privateKeys.pem" and "publicKeys.pem".

This will be distributed through the datasafe team.

```bash
kubectl create secret generic datasafe-keys --from-file=privateKey.pem --from-file=publicKey.pem
```