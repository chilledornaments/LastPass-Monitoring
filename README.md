# LastPass-Monitoring
Monitor user activity with the LastPass Enterprise API

You'll need an API key ("provisioning hash" as LastPass calls it) and you CID. Not sure what the CID is but you can find both at https://lastpass.com/company/#!/settings/enterprise-api.

You could pretty easily extend this to log _not_ to Graylog. If you want to send this info to Graylog, you'll need `pygelf` installed (`pip3 install pygelf`) and a running UDP input.

I run this every 15 minutes. 