# bd-ponno

Scrapy MongoDB Django integrated API that scrapes popular e-commerce sites (10+) from Bangladesh.\
Added some extra functionalities for the API, ex- custom price and product tag filter

## Built With
```
Django==3.1.7
django-cors-headers==3.7.0
django-filter==2.4.0
django-heroku==0.3.1
djangorestframework==3.12.2
djongo==1.3.4
Scrapy==2.4.1
scrapy-djangoitem==1.1.1
pymongo==3.11.3
```

### Remarks
MongoDB Atlas is not a good option for djongo or remote web scraping, because djongo is just a connector for the underlying relational mapper with Django which causes additional delay, hence bad performance for remote scraping with Atlas.
Also, there could be some unintentional issues, for example - 

I ran into error to check product details view in admin panel because of its `ArrayReferenceField` class (`Category` model)

<details>
<summary>Click to view the error</summary>

```
AttributeError Exception Value:	 'list' object has no attribute '_meta'

trace the issue:
https://github.com/doableware/djongo/issues/136
```
</details>

### API preview

![bd_ponno_products](https://user-images.githubusercontent.com/40615350/157366690-1a3823e3-9599-4ed2-82dc-46013310906f.png)
