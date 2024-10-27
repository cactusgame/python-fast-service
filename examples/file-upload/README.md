# A demo for file upload

## calling 
```
curl --location --request POST 'localhost:2333/api/demo' \
--header 'Content-Type: multipart/form-data; boundary=--------------------------994702659308423812684350' \
--form 'more_args=777' \
--form 'the_uploaded_file=@/private/tmp/f.txt'
```
