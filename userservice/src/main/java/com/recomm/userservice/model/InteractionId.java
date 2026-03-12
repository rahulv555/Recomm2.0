package com.recomm.userservice.model;

import java.io.Serializable;
import java.util.Objects;

public class InteractionId implements Serializable {
    private String userID;
    private String placeID;

    // Default constructor, Getters, Setters, hashCode, and equals are REQUIRED
    public InteractionId() {}

    public InteractionId(String userID, String placeID) {
        this.userID = userID;
        this.placeID = placeID;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        InteractionId that = (InteractionId) o;
        return Objects.equals(userID, that.userID) && Objects.equals(placeID, that.placeID);
    }

    @Override
    public int hashCode() {
        return Objects.hash(userID, placeID);
    }
}