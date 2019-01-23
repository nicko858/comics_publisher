# Comics publisher

This script provides you ability to automatic posting [xkcd-comics](https://xkcd.com/) on [vk.com](https://vk.com).

The script uses following external API's: 
- [xkcd-api](https://xkcd.com/info.0.json)
- [vk-api](https://api.vk.com) 

If everything is fine, you'll see a new post in your `vk-group` with a random comics:

![027.png](https://github.com/nicko858/comics_publisher/blob/master/screenshots/%D0%92%D1%8B%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_027.png)

### How to install
Python3 should be already installed.
```bash
$ git clone https://github.com/nicko858/comics_publisher.git
$ cd comics_publisher
$ pip install -r requirements.txt
```

- Create account on the [vk.com](https://vk.com), or use existing
- Create fan-group where you will posting comics - [vk group management](https://vk.com/groups?tab=admin)
- Register new application following this [link](https://vk.com/apps?act=manage)
- Make sure, that application is turned on and remember it's `application_id`:
![023.png](https://github.com/nicko858/comics_publisher/blob/master/screenshots/%D0%92%D1%8B%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_023.png)
- Link application with group created on the previous step:
![024.png](https://github.com/nicko858/comics_publisher/blob/master/screenshots/%D0%92%D1%8B%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_024.png)
- Get `access_token` using [Implicit Flow](https://vk.com/dev/implicit_flow_user):

![025.png](https://github.com/nicko858/comics_publisher/blob/master/screenshots/%D0%92%D1%8B%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5_025.png)

and remember it
- Create file `.env` in the script directory
- Add the following records to the `.env-file`:
   - client_id=`Your application_id`
   - access_token=`Your access token`
   - vk_group_id=`Your vk_group_id`

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
