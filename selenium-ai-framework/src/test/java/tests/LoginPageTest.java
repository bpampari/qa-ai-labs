package tests;

import base.BaseTest;
import org.testng.annotations.Test;
import pages.LoginPage;


public class LoginPageTest extends BaseTest {

    @Test
    public void validLoginTest() {

        LoginPage login = new LoginPage(driver);

        login.open();
        login.login("Admin", "admin123");
    }
}
