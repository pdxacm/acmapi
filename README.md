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
        "http://acm.pdx.edu/api/v1/events/<int:event_id>"
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
        "http://acm.pdx.edu/api/v1/posts/<int:post_id>"
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
$ curl http://acm.pdx.edu/api/v1/memberships/1
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

### Events

#### Add Events

```sh
$ curl http://acm.pdx.edu/api/v1/events/ \
    -d title="Event Title 1" \
    -d description="Event 1" \
    -d location="Room 1" \
    -d speaker="Bob" \
    -d start="2014-10-10 20:20:00.00000" \
    -d end="2014-10-10 21:10:00.00000"
```

```json
{
    "canceled": false, 
    "description": "Event 1", 
    "edited_at": "Mon, 21 Apr 2014 04:12:35 -0000", 
    "editor": "http://acm.pdx.edu/api/v1/people/1", 
    "editor_id": 1, 
    "end": "Fri, 10 Oct 2014 21:10:00 -0000", 
    "event_id": 1, 
    "hidden": false, 
    "location": "Room 1", 
    "revision": 1, 
    "speaker": "Bob", 
    "start": "Fri, 10 Oct 2014 20:20:00 -0000", 
    "title": "Event Title 1"
}
```

```sh
$ curl http://acm.pdx.edu/api/v1/events/ \
    -d title="Event Title 2" \
    -d description="Event 2" \
    -d location="Room 2" \
    -d speaker="Alex" \
    -d start="2014-11-10 20:20:00.00000" \
    -d end="2014-11-10 21:10:00.00000"
```

```json
{
    "canceled": false, 
    "description": "Event 2", 
    "edited_at": "Mon, 21 Apr 2014 04:14:42 -0000", 
    "editor": "http://acm.pdx.edu/api/v1/people/1", 
    "editor_id": 1, 
    "end": "Mon, 10 Nov 2014 21:10:00 -0000", 
    "event_id": 2, 
    "hidden": false, 
    "location": "Room 2", 
    "revision": 1, 
    "speaker": "Alex", 
    "start": "Mon, 10 Nov 2014 20:20:00 -0000", 
    "title": "Event Title 2"
}
```

#### Update Events by id

```sh
$ curl http://acm.pdx.edu/api/v1/events/1 -d canceled=True
```

```json
{
    "canceled": true, 
    "description": "Event 1", 
    "edited_at": "Mon, 21 Apr 2014 04:16:35 -0000", 
    "editor": "http://acm.pdx.edu/api/v1/people/1", 
    "editor_id": 1, 
    "end": "Fri, 10 Oct 2014 21:10:00 -0000", 
    "event_id": 1, 
    "hidden": false, 
    "location": "Room 1", 
    "revision": 2, 
    "speaker": "Bob", 
    "start": "Fri, 10 Oct 2014 20:20:00 -0000", 
    "title": "Event Title 1"
}
```

#### List all Events

```sh
$ curl http://acm.pdx.edu/api/v1/events/
```

```json
[
    {
        "canceled": true, 
        "description": "Event 1", 
        "edited_at": "Mon, 21 Apr 2014 04:16:35 -0000", 
        "editor": "http://acm.pdx.edu/api/v1/people/1", 
        "editor_id": 1, 
        "end": "Fri, 10 Oct 2014 21:10:00 -0000", 
        "event_id": 1, 
        "hidden": false, 
        "location": "Room 1", 
        "revision": 2, 
        "speaker": "Bob", 
        "start": "Fri, 10 Oct 2014 20:20:00 -0000", 
        "title": "Event Title 1"
    }, 
    {
        "canceled": false, 
        "description": "Event 2", 
        "edited_at": "Mon, 21 Apr 2014 04:14:42 -0000", 
        "editor": "http://acm.pdx.edu/api/v1/people/1", 
        "editor_id": 1, 
        "end": "Mon, 10 Nov 2014 21:10:00 -0000", 
        "event_id": 2, 
        "hidden": false, 
        "location": "Room 2", 
        "revision": 1, 
        "speaker": "Alex", 
        "start": "Mon, 10 Nov 2014 20:20:00 -0000", 
        "title": "Event Title 2"
    }
]
```

#### List all Event revisions by id

```sh
$ curl http://acm.pdx.edu/api/v1/events/1
```

```json
[
    {
        "canceled": false, 
        "description": "Event 1", 
        "edited_at": "Mon, 21 Apr 2014 04:12:35 -0000", 
        "editor": "http://acm.pdx.edu/api/v1/people/1", 
        "editor_id": 1, 
        "end": "Fri, 10 Oct 2014 21:10:00 -0000", 
        "event_id": 1, 
        "hidden": false, 
        "location": "Room 1", 
        "revision": 1, 
        "speaker": "Bob", 
        "start": "Fri, 10 Oct 2014 20:20:00 -0000", 
        "title": "Event Title 1"
    }, 
    {
        "canceled": true, 
        "description": "Event 1", 
        "edited_at": "Mon, 21 Apr 2014 04:16:35 -0000", 
        "editor": "http://acm.pdx.edu/api/v1/people/1", 
        "editor_id": 1, 
        "end": "Fri, 10 Oct 2014 21:10:00 -0000", 
        "event_id": 1, 
        "hidden": false, 
        "location": "Room 1", 
        "revision": 2, 
        "speaker": "Bob", 
        "start": "Fri, 10 Oct 2014 20:20:00 -0000", 
        "title": "Event Title 1"
    }
]
```

### Posts

#### Add Posts

```sh
$ curl http://acm.pdx.edu/api/v1/posts/ \
    -d title="This is the Title" \
    -d description="This is the description" \
    -d content="This is the content" 
```

```json
{
    "content": "This is the content", 
    "description": "This is the description", 
    "edited_at": "Mon, 21 Apr 2014 04:26:59 -0000", 
    "editor": "http://acm.pdx.edu/api/v1/people/1", 
    "editor_id": 1, 
    "hidden": false, 
    "post_id": 1, 
    "revision": 1, 
    "title": "This is the Title"
}
```

```sh
$ curl http://acm.pdx.edu/api/v1/posts/ \
    -d title="This is another Title" \
    -d description="This is another description" \
    -d content="This is some more content" 
```

```json
{
    "content": "This is some more content", 
    "description": "This is another description", 
    "edited_at": "Mon, 21 Apr 2014 04:29:07 -0000", 
    "editor": "http://acm.pdx.edu/api/v1/people/1", 
    "editor_id": 1, 
    "hidden": false, 
    "post_id": 2, 
    "revision": 1, 
    "title": "This is another Title"
}
```

#### Update Posts by id

```sh
$ curl http://acm.pdx.edu/api/v1/posts/1 -d canceled=True
```

```json
{
    "content": "This is the content", 
    "description": "This is the description", 
    "edited_at": "Mon, 21 Apr 2014 04:30:12 -0000", 
    "editor": "http://acm.pdx.edu/api/v1/people/1", 
    "editor_id": 1, 
    "hidden": false, 
    "post_id": 1, 
    "revision": 2, 
    "title": "This is the Title"
}
```

#### List all Posts

```sh
$ curl http://acm.pdx.edu/api/v1/posts/
```

```json
[
    {
        "content": "This is the content", 
        "description": "This is the description", 
        "edited_at": "Mon, 21 Apr 2014 04:30:12 -0000", 
        "editor": "http://acm.pdx.edu/api/v1/people/1", 
        "editor_id": 1, 
        "hidden": false, 
        "post_id": 1, 
        "revision": 2, 
        "title": "This is the Title"
    }, 
    {
        "content": "This is some more content", 
        "description": "This is another description", 
        "edited_at": "Mon, 21 Apr 2014 04:29:07 -0000", 
        "editor": "http://acm.pdx.edu/api/v1/people/1", 
        "editor_id": 1, 
        "hidden": false, 
        "post_id": 2, 
        "revision": 1, 
        "title": "This is another Title"
    }
]
```

#### List all Posts revisions by id

```sh
$ curl http://acm.pdx.edu/api/v1/posts/1
```

```json
[
    {
        "content": "This is the content", 
        "description": "This is the description", 
        "edited_at": "Mon, 21 Apr 2014 04:26:59 -0000", 
        "editor": "http://acm.pdx.edu/api/v1/people/1", 
        "editor_id": 1, 
        "hidden": false, 
        "post_id": 1, 
        "revision": 1, 
        "title": "This is the Title"
    }, 
    {
        "content": "This is the content", 
        "description": "This is the description", 
        "edited_at": "Mon, 21 Apr 2014 04:30:12 -0000", 
        "editor": "http://acm.pdx.edu/api/v1/people/1", 
        "editor_id": 1, 
        "hidden": false, 
        "post_id": 1, 
        "revision": 2, 
        "title": "This is the Title"
    }
]
```
