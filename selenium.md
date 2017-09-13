```python
##########################################################################################################
# get_attribute() get the attribute in selenium 
def test_chart_renders_from_url(self):
    url = 'http://localhost:8000/analyse/'
    self.browser.get(url)
    org = driver.find_element_by_id('org')
    # Find the value of org?
    val = org.get_attribute("attribute name")
```
