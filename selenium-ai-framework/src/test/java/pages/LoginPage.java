package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class LoginPage {

    private WebDriver driver;
    private WebDriverWait wait;

    public LoginPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    private By username = By.name("uddssername");
    private By password = By.name("password");
    private By loginBtn = By.xpath("//button[@type='submit']");

    public void open() {
        driver.get("https://opensource-demo.orangehrmlive.com/");
    }

    public void login(String user, String pass) {

        wait.until(ExpectedConditions.visibilityOfElementLocated(username))
                .sendKeys(user);

        wait.until(ExpectedConditions.visibilityOfElementLocated(password))
                .sendKeys(pass);

        wait.until(ExpectedConditions.elementToBeClickable(loginBtn))
                .click();
    }
}