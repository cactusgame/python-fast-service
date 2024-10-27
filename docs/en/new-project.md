# How to Create a New Project

## Manual Creation

Use the `examples/simple` project as a template for creating a new project. Execute the following commands in the framework root directory. The steps are detailed below:

- Create a new project named `hello-world` by copying the `examples/simple` project to the desired location (in this example, the `tmp` directory).

```bash
cp -r examples/simple /tmp/hello-world
```

- Replace all instances of the string `simple` with `hello-world`. (The following command can be run on a Mac.)

```bash
find /tmp/hello-world/ -name \*.py -o -name \*.sh -o -name \*.md | xargs grep -l "simple" | xargs sed -i '' 's/simple/hello-world/g'
```

# Starting the Service

Whether you use the `automatic creation` or `manual creation` method for your project, you’ll need to install the dependencies listed in `setup/base.txt` before starting the service.

```bash
cd /tmp/hello-world

pfs
```
