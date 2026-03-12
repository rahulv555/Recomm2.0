package com.recomm.restaurantservice.dto;



public class RestaurantResponseDTO {
    private String placeID;

    private Double latitude;

    private Double longitude;

    private String name;

    private String address;
    
    private String state;

    private String country;

    private String alcohol;

    private String smoking_area;

    private String dress_code;

    private String accessibility;

    private String price;

    private String rambience;

    private String franchise;

    private String area;
    
    private String parking_lot;

    private String[] Rcuisine;
    public String getPlaceID() {
    return placeID;
}

public void setPlaceID(String placeID) {
    this.placeID = placeID;
}

    public String getPlaceName() {
    return name;
}

    public Double getLatitude() {
    return latitude;
}

public void setLatitude(Double latitude) {
    this.latitude = latitude;
}

public Double getLongitude() {
    return longitude;
}

public void setLongitude(Double longitude) {
    this.longitude = longitude;
}

public String getName() {
    return name;
}

public void setName(String name) {
    this.name = name;
}

public String getAddress() {
    return address;
}

public void setAddress(String address) {
    this.address = address;
}

public String getState() {
    return state;
}

public void setState(String state) {
    this.state = state;
}

public String getCountry() {
    return country;
}

public void setCountry(String country) {
    this.country = country;
}

public String getAlcohol() {
    return alcohol;
}

public void setAlcohol(String alcohol) {
    this.alcohol = alcohol;
}

public String getSmoking_area() {
    return smoking_area;
}

public void setSmoking_area(String smoking_area) {
    this.smoking_area = smoking_area;
}

public String getDress_code() {
    return dress_code;
}

public void setDress_code(String dress_code) {
    this.dress_code = dress_code;
}

public String getAccessibility() {
    return accessibility;
}

public void setAccessibility(String accessibility) {
    this.accessibility = accessibility;
}

public String getPrice() {
    return price;
}

public void setPrice(String price) {
    this.price = price;
}

public String getRambience() {
    return rambience;
}

public void setRambience(String rambience) {
    this.rambience = rambience;
}

public String getFranchise() {
    return franchise;
}

public void setFranchise(String franchise) {
    this.franchise = franchise;
}

public String getArea() {
    return area;
}

public void setArea(String area) {
    this.area = area;
}

public String getParking_lot() {
    return parking_lot;
}

public void setParking_lot(String parking_lot) {
    this.parking_lot = parking_lot;
}

public String[] getRcuisine() {
    return Rcuisine;
}

public void setRcuisine(String[] rcuisine) {
    Rcuisine = rcuisine;
}
}
