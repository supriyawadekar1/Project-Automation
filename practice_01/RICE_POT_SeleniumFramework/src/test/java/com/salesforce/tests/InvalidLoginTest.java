package com.salesforce.tests;

import org.testng.Assert;
import org.testng.annotations.Test;

import com.salesforce.base.BaseTest;

public class InvalidLoginTest extends BaseTest {

    @Test
    public void testInvalidLoginWrongPassword() {
        try {
            loginPage.doLogin("invaliduser@example.com", "WrongPassword123!");
            Assert.assertTrue(loginPage.isErrorMessageDisplayed(), "Error message not displayed for wrong password");
        } catch (AssertionError e) {
            throw e;
        } catch (Exception e) {
            Assert.fail("Exception during wrong password login: " + e.getMessage());
        }
    }

    @Test
    public void testInvalidLoginEmptyUsername() {
        try {
            loginPage.doLogin("", "SomePassword123!");
            Assert.assertTrue(loginPage.isErrorMessageDisplayed(), "Error message not displayed for empty username");
        } catch (AssertionError e) {
            throw e;
        } catch (Exception e) {
            Assert.fail("Exception during empty username login: " + e.getMessage());
        }
    }

    @Test
    public void testInvalidLoginEmptyPassword() {
        try {
            loginPage.doLogin("invaliduser@example.com", "");
            Assert.assertTrue(loginPage.isErrorMessageDisplayed(), "Error message not displayed for empty password");
        } catch (AssertionError e) {
            throw e;
        } catch (Exception e) {
            Assert.fail("Exception during empty password login: " + e.getMessage());
        }
    }

    @Test
    public void testInvalidLoginBothEmpty() {
        try {
            loginPage.doLogin("", "");
            Assert.assertTrue(loginPage.isErrorMessageDisplayed(), "Error message not displayed for both empty fields");
        } catch (AssertionError e) {
            throw e;
        } catch (Exception e) {
            Assert.fail("Exception during both empty login: " + e.getMessage());
        }
    }

    @Test
    public void testInvalidLoginInvalidEmailFormat() {
        try {
            loginPage.doLogin("invalid-email-format", "SomePassword123!");
            Assert.assertTrue(loginPage.isErrorMessageDisplayed(), "Error message not displayed for invalid email format");
        } catch (AssertionError e) {
            throw e;
        } catch (Exception e) {
            Assert.fail("Exception during invalid email format login: " + e.getMessage());
        }
    }
}
