# Bundling the Example Problems

So far, we have created three challenges for our competition. On this page,
we're going to discuss how to bundle these challenges into one package
and the benefits of doing so.

A bundle is simply a group of challenges that can be distributed as one package.
Additionally, bundles allow you to specify the unlocking procedure for your challenges.

## Creating the Bundle

We will create a bundle containing our three example challenges. Creating a bundle requires
only a `bundle.json` file, as shown below.

```json
{
  "name": "Train the Trainer Sampler",
  "author": "YOUR NAME HERE",
  "description": "A set of challenges created for Train the Trainer.",
  "categories": ["Binary Exploitation", "Cryptography", "Web Exploitation"],
  "problems": ["buffer-overflow-1", "ecb-encryption", "sql-injection-1"],
  "dependencies": {
    "ecb-encryption": {
      "threshold": 1,
      "weightmap": {
        "buffer-overflow-1": 1
      }
    },
    "sql-injection-1": {
      "threshold": 1,
      "weightmap": {
        "buffer-overflow-1": 1,
        "ecb-encryption": 1
      }
    }
  }
}
```

This `bundle.json` specifies all of the information needed to create a bundle. Be
sure to check out the [bundle.json Specification](..//bundle-json-spec.md)
to see the optional fields.

Be sure that you have installed all of the problem `.deb` files created previously.
Once you have done so, you can run `sudo shell_manager bundle bundle.json` to create
your bundled deb package.

You should continue by installing your bundle deb package as well, using
`sudo dpkg -i ctf-train-the-trainer-sampler-bundle-1.0-0.deb`. This will make the bundle information available
to the `shell_manager`.

## Deploying the Bundle

Once we've installed the bundle, we can deploy 3 instances of each of our challenges
using `sudo shell_manager deploy -b train-the-trainer-sampler -n 3`.
