acmapi
======

[![Build Status](https://travis-ci.org/cameronbwhite/acmapi.png?branch=master)](https://travis-ci.org/cameronbwhite/acmapi)

API for the @acmpdx

## Examples

### Top Level

```sh
$ curl http://acm.pdx.edu/api/v1/
```

```json
{
    "events_url": [
        "http://acm.pdx.edu/api/v1/events/"
    ], 
    "memberships_url": [
        "http://acm.pdx.edu/api/v1/memberships/", 
        "http://acm.pdx.edu/api/v1/memberships/<int:membership_id>"
    ], 
    "officerships_url": [
        "http://acm.pdx.edu/api/v1/officerships/", 
        "http://acm.pdx.edu/api/v1/officerships/<int:officership_id>"
    ], 
    "people_url": [
        "http://acm.pdx.edu/api/v1/people/", 
        "http://acm.pdx.edu/api/v1/people/<int:person_id>", 
        "http://acm.pdx.edu/api/v1/people/<int:editor_id>", 
        "http://acm.pdx.edu/api/v1/people/<string:username>"
    ], 
    "posts_url": [
        "http://acm.pdx.edu/api/v1/posts/"
    ]
}
```

### People

#### Add a person

```sh
$ curl http://acm.pdx.edu/api/v1/people/ \
    -d username="foobar" \
    -d name="Foo Bar" \
    -d email="foobar@example.com"
```

```json
{
    "email": "foobar@example.com", 
    "id": 2, 
    "name": "Foo Bar", 
    "username": "foobar", 
    "website": null
}
```

#### Add a second user

```sh
$ curl http://acm.pdx.edu/api/v1/people/ -d username="war5" 
```

```json
{
    "email": null, 
    "id": 2, 
    "name": null, 
    "username": "war5", 
    "website": null
}
```

#### Update user by username

```sh
$ curl http://acm.pdx.edu/api/v1/people/war5 -d name="Billy Bob" 
```

```json
{
    "email": null, 
    "id": 2, 
    "name": "Billy Bob", 
    "username": "war5", 
    "website": null
}
```

#### Update user by id

```sh
$ curl http://acm.pdx.edu/api/v1/people/war5 \
    -d email="billybob@example.com" 
```

```json
{
    "email": "billybob@example.com", 
    "id": 2, 
    "name": "Billy Bob", 
    "username": "war5", 
    "website": null
}
```

#### List all users

```sh
$ curl http://acm.pdx.edu/api/v1/people/
```

```json
[
    {
        "email": null, 
        "id": 1, 
        "name": "Foo Bar", 
        "username": "foobar", 
        "website": null
    }, 
    {
        "email": "billybob@example.com",
        "id": 2, 
        "name": "Billy Bob", 
        "username": "war5", 
        "website": null
    }
]
```

#### Find people by id

```sh
$ curl http://acm.pdx.edu/api/v1/people/1
```

```json
{
    "email": null, 
    "id": 1, 
    "name": "Foo Bar", 
    "username": "foobar", 
    "website": null
}
```

#### Find people by username

```sh
$ curl http://acm.pdx.edu/api/v1/people/foobar
```

```json
{
    "email": null, 
    "id": 1, 
    "name": "Foo Bar", 
    "username": "foobar", 
    "website": null
}
```

#### Delete people by username

```sh
$ curl -X DELETE http://acm.pdx.edu/api/v1/people/foobar
```

```json
{
    "message": "delete successful"
}
```

#### Delete people by id

```sh
$ curl -X DELETE http://acm.pdx.edu/api/v1/people/1
```

```json
{
    "message": "delete successful"
}
```

### Memberships

#### Add membership to user

```sh
$ curl http://acm.pdx.edu/api/v1/memberships/ \
    -d person_id=1 \
    -d start_date="2014-10-11" \
    -d end_date="2015-10-11"
```

```json
{
    "end_date": "2015-10-11", 
    "id": 1, 
    "person": "http://acm.pdx.edu/api/v1/people/1", 
    "person_id": 1, 
    "start_date": "2014-10-11"
}
```

#### List all memberships

```sh
$ curl http://acm.pdx.edu/api/v1/memberships/
```

```json
[
    {
        "end_date": "2015-10-11", 
        "id": 1, 
        "person": "http://acm.pdx.edu/api/v1/people/1", 
        "person_id": 1, 
        "start_date": "2014-10-11"
    }
]
```

#### Find membership by id 

```sh
$ cul http://acm.pdx.edu/api/v1/memberships/1
```

```json
{
    "end_date": "2015-10-11", 
    "id": 1, 
    "person": "http://acm.pdx.edu/api/v1/people/1", 
    "person_id": 1, 
    "start_date": "2014-10-11"
}
```

#### Delete membership by id

```sh
$ curl -X DELETE http://acm.pdx.edu/api/v1/memberships/1
```

```json
{
    "message": "delete successful"
}
```

### Officerships

#### Add officerships to user

```sh
$ curl http://acm.pdx.edu/api/v1/officerships/ \
    -d person_id=1 \
    -d title="Vice Chair" \
    -d start_date="2014-10-11" \
    -d end_date="2015-10-11"
```

```json
{
    "end_date": "2015-10-11", 
    "id": 1, 
    "person": "http://acm.pdx.edu/api/v1/people/1", 
    "person_id": 1, 
    "start_date": "2014-10-11",
    "title": "Vice Chair"
}
```

#### List all officerships

```sh
$ curl http://acm.pdx.edu/api/v1/officerships/
```

```json
[
    {
        "end_date": "2015-10-11", 
        "id": 1, 
        "person": "http://acm.pdx.edu/api/v1/people/1", 
        "person_id": 1, 
        "start_date": "2014-10-11",
        "title": "Vice Chair"
    }
]
```

#### Find officerships by id 

```sh
$ curl http://acm.pdx.edu/api/v1/officerships/1
```

```json
{
    "end_date": "2015-10-11", 
    "id": 1, 
    "person": "http://acm.pdx.edu/api/v1/people/1", 
    "person_id": 1, 
    "start_date": "2014-10-11",
    "title": "Vice Chair"
}
```

#### Delete membership by id

```sh
$ curl -X DELETE http://acm.pdx.edu/api/v1/officerships/1
```

```json
{
    "message": "delete successful"
}
```
