package com.recomm.restaurantservice.model;

import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "places")
public class Restaurant {
    @Id
    @Column(updatable = false, nullable = false)
    private String placeID;

    @NotNull
    @Column
    private Double latitude;

    @NotNull
    @Column
    private Double longitude;

    @NotNull
    @Column
    private String name;

    @NotNull
    @Column
    private String address;

    
    @NotNull
    @Column
    private String state;

    @NotNull
    @Column
    private String country;

    @NotNull
    @Column
    private String alcohol;

    @NotNull
    @Column
    private String smoking_area;

    @NotNull
    @Column
    private String dress_code;

    @NotNull
    @Column
    private String accessibility;

    @NotNull
    @Column
    private String price;

    @NotNull
    @Column
    private String rambience;

    @NotNull
    @Column
    private String franchise;

    @NotNull
    @Column
    private String area;
    
    @NotNull
    @Column
    private String parking_lot;

    @Column
    private String[] Rcuisine;

    public String getPlaceID() {
    return placeID;
}

public void setPlaceID(String placeID) {
    this.placeID = placeID;
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
