# Tencent Meeting Tool

## Get cookie

First you need to get the login cookie.

Log in at the URL below [qrcode-login](https://meeting.tencent.com/qrcode-login.html).

After login, open the console or find the corresponding value in the browser's cookie and copy it.

Just set the cookie value to the environment variable.

## Usage

### Quick join

Just enter 'jm' and the conference code, for example:

`jm 111-111-111`

`jm 111111111`

### Quick create meeting

#### Create quick meeting

You can also reset the default meeting name.

Just type `cm`.

#### Create meeting

Here are some optional parameters for creating a more cumbersome meeting.

- Specify the name of the meeting

`-n meeting_name`

- Specify the password of the meeting

`-p password`

- Set meeting Time

`-m 30`

- Set When to start the meeting, it is in the format of %Y-%m-%d/%H:%M.

`-t 2023-11-09/12:30`

- Set When to start the meeting, it is in the format of %H:%M.

`-t 12:30`

- Set When to start the meeting, a few hours later.

`-t 1h`

- Set When to start the meeting, a few minutes later.

`-t 30m`
