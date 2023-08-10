# Passman
## DESCRIPTION:
Pandora discovered the presence of a mole within the ministry. To proceed with caution, she must obtain the master control password for the ministry, which is stored in a password manager. Can you hack into the password manager?
## HINT:
- NONE
## STEPS:
1. Analyzing the `entrypoint.sh`, it seems the objective is to login as admin, because the flag is hardcoded there, and we can't login easily as admin, because the password is the flag.

> SNIPPET OF ENTRYPOINT.SH
```sh
INSERT INTO passman.saved_passwords (owner, type, address, username, password, note)
VALUES
    ('admin', 'Web', 'igms.htb', 'admin', 'HTB{f4k3_fl4g_f0r_t3st1ng}', 'password'),
    ('louisbarnett', 'Web', 'spotify.com', 'louisbarnett', 'YMgC41@)pT+BV', 'student sub'),
    ('louisbarnett', 'Email', 'dmail.com', 'louisbarnett@dmail.com', 'L-~I6pOy42MYY#y', 'private mail'),
    ('ninaviola', 'Web', 'office365.com', 'ninaviola1', 'OfficeSpace##1', 'company email'),
    ('alvinfisher', 'App', 'Netflix', 'alvinfisher1979', 'efQKL2pJAWDM46L7', 'Family Netflix'),
    ('alvinfisher', 'Web', 'twitter.com', 'alvinfisher1979', '7wYz9pbbaH3S64LG', 'old twitter account');

GRANT ALL ON passman.* TO 'passman'@'%' IDENTIFIED BY 'passman' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

/usr/bin/supervisord -c /etc/supervisord.conf
```

2. Notice the webapp using graphql to manage interactions with the database, knowing it uses graphql, hence the approach here unlikely to be sqli.
3. Anyway after analyzed the `GraphqlHelper.js`, notice the `UpdatePassword` mutation does not require any validation.

```js
UpdatePassword: {
            type: ResponseType,
            args: {
                username: { type: new GraphQLNonNull(GraphQLString) },
                password: { type: new GraphQLNonNull(GraphQLString) }
            },
            resolve: async (root, args, request) => {
                return new Promise((resolve, reject) => {
                    if (!request.user) return reject(new GraphQLError('Authentication required!'));

                    db.updatePassword(args.username, args.password)
                        .then(() => resolve(response("Password updated successfully!")))
                        .catch(err => reject(new GraphQLError(err)));
                });
            }
        },
```

4. It accepts both username and password, but not checks who we are. Seems the vuln here is IDOR.

### FLOW

**REMEMBER THE VULN IS IDOR**
```
- It's very straightforward, we just need to make an account, then login.
- Next we intercept the request to refresh the page using burpsuite and grab our cookie.
- Logout and intercept the login request.
- At the request tab, we change the mutation to UpdatePassword, the username to admin, and the password as random character.
- Then we use the cred to login --> get flag.
```

5. Let's try that.

> INTERCEPT REQUEST --> CHANGE THE MUTATION TO UPDATE PASSWORD AND THE CREDS.

![Untitled](https://github.com/jon-brandy/hackthebox/assets/70703371/3c5bdcae-f59e-44bb-aa9f-23869c57a51b)



> LOGIN

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5c345e9b-a2fb-4466-906d-25cd8e748b69)


6. Got the flag!

## FLAG

```
HTB{n0_acc3ss_c0ntr0ls_id0r_pwn4g3!!}
```
