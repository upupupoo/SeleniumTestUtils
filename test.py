from UIutils import *
from helium import *
driver=DriverTool.create_driver()
set_driver(driver)
go_to('https://www.baidu.com/')
HeliumTool.hewrite('123',HeliumTool.s('#kw'))
