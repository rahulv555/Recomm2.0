package com.recomm.restaurantservice.dto;

import java.util.List;

public class RestaurantListRequestDTO {

    private List<String> placeIDs;

    public List<String> getPlaceIDs() {
        return placeIDs;
    }

    public void setPlaceIDs(List<String> placeIDs) {
        this.placeIDs = placeIDs;
    }
}