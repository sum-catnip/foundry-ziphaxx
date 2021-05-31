# Foundry arbitrary directory overwrite POC expoit

More info: http://catnip.fyi/posts/foundry-p1/

I know i suck at naming things, no need to tell me.

This exploit allows you to overwrite arbitrary directories on an unpatched target foundry
server.

it works like this:
- zip up the `in` dir
- make a module.json where the name field contains the target path ex: `../kektop`
- make a post request to /setup with action: installPackage and the manifest pointing to our evil module.json

This is how you use it:
- get an admin session with my other exploit (releasing soon TM)
- put some malicious data in the `in` dir
- run exploit against target:
> python ziphaxx.py http://localhost:30000
- start http server in out dir:
> python -m http.server 1337
- specify target dir: ../kektop

The exploit will also guide you through those steps.
