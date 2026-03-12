package com.recomm.restaurantservice.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.IdClass;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "interactions")
@IdClass(InteractionId.class)
public class Interaction {

    @Id
    @Column(updatable = false, nullable = false)
    private String userID;

    @Id
    @Column(updatable = false, nullable = false)
    private String placeID;

    @NotNull
    @Column
    private Double rating;

    @NotNull
    @Column
    private Double food_rating;

    @NotNull
    @Column
    private Double service_rating;


    public String getUserId() {
    return userID;
}

public void setUserId(String userID) {
    this.userID = userID;
}

    public String getPlaceId() {
    return placeID;
}

public void setPlaceId(String placeID) {
    this.placeID = placeID;
}

public Double getRating() {
    return rating;
}

public void setRating(Double rating) {
    this.rating = rating;
}

public Double getFoodRating() {
    return food_rating;
}

public void setFoodRating(Double food_rating) {
    this.food_rating = food_rating;
}

public Double getServiceRating() {
    return service_rating;
}

public void setServiceRating(Double service_rating) {
    this.service_rating = service_rating;
}

}
