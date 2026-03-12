package com.recomm.userservice.dto;

public class RatePlaceDTO {
    private String placeID;

    

    private Double rating;

    private Double foodRating;

    private Double serviceRating;

    public String getPlaceID() {
    return placeID;
}

public void setPlaceID(String placeID) {
    this.placeID = placeID;
}

public Double getRating() {
    return rating;
}

public void setRating(Double rating) {
    this.rating = rating;
}

public Double getFoodRating() {
    return foodRating;
}

public void setFoodRating(Double foodRating) {
    this.foodRating = foodRating;
}

public Double getServiceRating() {
    return serviceRating;
}

public void setServiceRating(Double serviceRating) {
    this.serviceRating = serviceRating;
}


}
