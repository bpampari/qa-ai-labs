package tests;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.Test;

import base.BaseTest;
import pages.LoginPage;

import java.time.Duration;

public class DashboardTest extends BaseTest {

    @Test
    public void testSuccessfulLogin() {
        // Login to the application using LoginPage
        LoginPage loginPage = new LoginPage(driver);
        loginPage.open();
        loginPage.login("Admin", "admin123");

        // Wait for the dashboard page to load
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        WebElement dashboardTitle = wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath("//h6[text()='Dashboard']")));

        // Verify the dashboard title text
        Assert.assertTrue(dashboardTitle.getText().equals("Dashboard"));

        // Add additional assertions if needed
    }
}