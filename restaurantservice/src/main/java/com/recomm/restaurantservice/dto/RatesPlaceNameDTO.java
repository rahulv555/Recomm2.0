package com.recomm.restaurantservice.dto;
public class RatesPlaceNameDTO {
private String name;
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

    public String getPlaceName() {
    return name;
}

public void setPlaceName(String name) {
    this.name = name;
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
