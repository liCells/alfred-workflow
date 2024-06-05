# Tencent Meeting Tool

Quickly join, create or cancel a meeting with Tencent Meeting.

## Usage

### Login

Enter `lm`, and press `shift` to display the login QR code.

After scanning, press enter to monitor whether the login succeeds in real time.

### Quick join

Just enter 'jm' and the conference code, for example:

`jm 111-111-111`

`jm 111111111`

Even if you enter a paragraph of text, the corresponding meeting number can be automatically extracted, if there is more than one meeting number, a list will be displayed, and you can press enter to enter the meeting. For example:

`jm meeting code: 111-111-111`

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

### Quick view meeting

Just type `vm`.

Press `Enter` to enter the meeting.

Press `Option+Enter` to copy the meeting-related information.

Press `Shift+Enter` to copy the meeting-related information.

Press `Command+Enter` to cancel the meeting.

### Quick cancel meeting

First view the meeting information through the `vm` command, Then cancel the meeting with `command + enter`.

### Custom create meeting result content

You can set the return value after creating a meeting through the `Meeting information` variable.

#### Below is an example

> meeting subject: {subject}
> 
> code: {meeting_code}
> 
> join url: {url}

#### available variables

- `{subject}` -> Meeting name
- `{begin_time}` -> meeting start time
- `{end_time}` -> meeting end time
- `{url}` -> Meeting link
- `{meeting_code}` -> meeting code

