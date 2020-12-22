# Webrunner

**Built using:** python w/ flask | html/js/css | sql

**Based on:** flask mega-tutorial from [miguel grinberg](https://blog.miguelgrinberg.com/index) | plus lots of inspiration from [psiturk](http://psiturk.org/)

**version:** 1.0

For a detailed outline of how to use the webrunner, see the [`the manual`](_/manual.md). Feel free to contact mwetzel2@binghamton.edu if you have any questions/issues (or use the issue tracker).



## Info

### [Kurtz Lab](http://kurtzlab.psychology.binghamton.edu/) Webrunner

This repo provides a basic setup for hosting online experiments via a flask webserver. It's **not at the stage of being a legitimate tool for development**; rather, it's a way to give anyone interested a head start on webprogramming for psychological research. If you choose to use it, you'll likely have to do a lot of learning and troubleshooting (unless you're already familiar with this sort of thing).

>  ^ while it's pretty bare-bones, it's been working fine for our lab's purposes

Things it handles are:

- hosting the webserver that handles traffic through whatever domain name you have access to
- loading multiple experiments sequentially
- condition assignment
- managing multiple users concurrently
- assigned credit through SONA, if using

---



## Dependencies

- [flask](https://flask.palletsprojects.com/en/1.1.x/) w/ addons:
    - [flask-login](https://flask-login.readthedocs.io/en/latest/) (for user login management)
    - [flask-sqlalchemy](https://flask-wtf.readthedocs.io/en/stable/) (for sql)
    - [flask-wtf](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) (for forms)
- [cryptography](https://cryptography.io/en/latest/) (for the Fernet function)
- [waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) (for deployment-ready server; feel free to use something else though)



## Resources

- see [`the manual`](_/manual.md) for instructions on how to use
- for building experiments, we typically just use the [ocanvas](http://ocanvas.org/) library. However, there are lots of web experiment libraries if you don't feel like coding experiments from scratch:
    - the [experiment factory](https://expfactory.github.io/) by [Vanessa Sochat](https://vsoch.github.io/)
        - ^ highly recommend looking here
    - psiturk's [experiment exchange](http://psiturk.org/ee/)
    - [jsPsych](https://www.jspsych.org/) by [Josh de Leeuw](https://www.vassar.edu/faculty/jdeleeuw/)
    - psychopy's [online toolkit](https://www.psychopy.org/#online) by [Jonathan Peirce](https://www.nottingham.ac.uk/psychology/people/jonathan.peirce)
- if you want to know more about how web programming works, check out this awesome tutorial from [miguel grinberg](https://blog.miguelgrinberg.com/index)
    - he's a very good programmer, and very good at explaining concepts underlying code examples

---



## Roadmap

- keep anonymous as the _default_ option

- more debugging / testing
  - this whole thing was put together kind of quickly and could definitely use more testing

---



## To Do List

- see if flask / flask-addons have any encryption tools to avoid needing to download the cryptography lib (<-- which is an awesome tool; but just an extra dep that might be worth shedding)
- if possible, make it so that if a subject logs out or quits the page, they'll get rerouting back to the experiment they're currently on when they try to log back in 

---



## Notes

**Version Change:** Version 0 was generally useful; we got around ~1500 datapoints using it (from about 500 subjects). A lot was repurposed in v1.0. 

- major changes in V1.0 are:
  - some general reorganizing
      - based on an impressive tutorial by miguel grinberg @ https://blog.miguelgrinberg.com/index
  - bringing on board the whole family of flask assets (e.g. sqlalchemy)
  - automatic experiment routing (based on experiment id)
  - condensed all data into 1 database (instead of 3)
      - not sure if i like human names being stored in the same spot as data ids
  - no sensitive data stored in localStorage; instead, everything's stored through the `flask-login`'s `current_user` tool
      - there is a link to the participant id and the subject's name that's stored as `temp_name_link` in the db, but it's encrypted, and the secret key is reset each time the webrunner is restarted (so it's functionally anonymous)
          - ^ unless of course you set `config.security` to `confidential` <-- in which case, it's no longer anonymous 
---