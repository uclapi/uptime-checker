# uptime-checker
Uptime checking scripts to be run on Lambda to keep our Cachet UI (status.uclapi.com) kept up to date

For passing parameters we can use a mapping for example
```{
    "uclapi_token":"$input.params('uclapi_token')",
    "cachet_token":"$input.params('cachet_token')"
}
```

And then when we call it pass in these parameters for example

```
https://awslambdaapiurl.../prod/-params?uclapi_token=uclapi-537547&cachet_token=our_cachet_token
```
