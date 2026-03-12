
package com.recomm.userservice.dto;

public class LoginUserResponseDTO {
    private boolean userExists;


    public boolean getUserExists() {
        return userExists;
    }

    public void setUserExists(boolean userExists) {
        this.userExists = userExists;
    }
}
