package com.salesforce.tests;

import org.testng.Assert;
import org.testng.annotations.Test;

import com.salesforce.base.BaseTest;
import com.salesforce.config.ConfigReader;

public class ValidLoginTest extends BaseTest {

    @Test
    public void testLoginPageElementsRendered() {
        try {
            Assert.assertTrue(loginPage.isUsernameDisplayed(), "Username field not displayed");
            Assert.assertTrue(loginPage.isPasswordDisplayed(), "Password field not displayed");
            Assert.assertTrue(loginPage.isLoginButtonDisplayed(), "Login button not displayed");
            Assert.assertTrue(loginPage.isRememberMeDisplayed(), "Remember me checkbox not displayed");
        } catch (AssertionError e) {
            throw e;
        } catch (Exception e) {
            Assert.fail("Exception while verifying login page elements: " + e.getMessage());
        }
    }

    @Test
    public void testValidLogin() {
        try {
            loginPage.doLogin(ConfigReader.getValidUsername(), ConfigReader.getValidPassword());
            Assert.assertTrue(driver.getCurrentUrl().contains("my.salesforce.com"),
                    "Login did not redirect to Salesforce home. Current URL: " + driver.getCurrentUrl());
        } catch (AssertionError e) {
            throw e;
        } catch (Exception e) {
            Assert.fail("Exception during valid login: " + e.getMessage());
        }
    }

    @Test
    public void testRememberMeCheckbox() {
        try {
            loginPage.checkRememberMe();
            Assert.assertTrue(loginPage.isRememberMeChecked(), "Remember me checkbox not checked after click");
        } catch (AssertionError e) {
            throw e;
        } catch (Exception e) {
            Assert.fail("Exception while verifying remember me checkbox: " + e.getMessage());
        }
    }
}
