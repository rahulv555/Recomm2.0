
package com.recomm.userservice.dto;

import java.util.List;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public class CreateUserRequestDTO {


    @NotBlank(message = "Name is required")
    @Size(max = 200, message = "Name cannot exceed 200 characters")
    private String name;

    @NotNull
    private String smoker;


    @NotNull
    private String drink_level;

    @NotNull
    private String budget;

    @NotNull
    private String dress_preference;

    @NotNull
    private String ambience;

    @NotNull
    private String transport;

    @NotNull
    private String marital_status;

    @NotNull
    private String hijos;

    @NotNull
    private String personality;

    @NotNull
    private String religion;

    @NotNull
    private String interest;
    
    @NotNull
    private String activity;

    @NotNull
    private String color;

    @NotNull
    private String[] cuisine;
    
    @NotNull
    private Double height;

    @NotNull
    private Double weight;

    @NotNull
    private Integer birth_year;

    @NotNull
    private Integer age;

    public String getName() {
    return name;
}

public void setName(String name) {
    this.name = name;
}

public String getSmoker() {
    return smoker;
}

public void setSmoker(String smoker) {
    this.smoker = smoker;
}

public String getDrink_level() {
    return drink_level;
}

public void setDrink_level(String drink_level) {
    this.drink_level = drink_level;
}

public String getBudget() {
    return budget;
}

public void setBudget(String budget) {
    this.budget = budget;
}

public String getDress_preference() {
    return dress_preference;
}

public void setDress_preference(String dress_preference) {
    this.dress_preference = dress_preference;
}

public String getAmbience() {
    return ambience;
}

public void setAmbience(String ambience) {
    this.ambience = ambience;
}

public String getTransport() {
    return transport;
}

public void setTransport(String transport) {
    this.transport = transport;
}

public String getMarital_status() {
    return marital_status;
}

public void setMarital_status(String marital_status) {
    this.marital_status = marital_status;
}

public String getHijos() {
    return hijos;
}

public void setHijos(String hijos) {
    this.hijos = hijos;
}

public String getPersonality() {
    return personality;
}

public void setPersonality(String personality) {
    this.personality = personality;
}

public String getReligion() {
    return religion;
}

public void setReligion(String religion) {
    this.religion = religion;
}

public String getInterest() {
    return interest;
}

public void setInterest(String interest) {
    this.interest = interest;
}

public String getActivity() {
    return activity;
}

public void setActivity(String activity) {
    this.activity = activity;
}

public String getColor() {
    return color;
}

public void setColor(String color) {
    this.color = color;
}

public String[] getCuisine() {
    return cuisine;
}

public void setCuisine(String[] cuisine) {
    this.cuisine = cuisine;
}

public Double getHeight() {
    return height;
}

public void setHeight(Double height) {
    this.height = height;
}

public Double getWeight() {
    return weight;
}

public void setWeight(Double weight) {
    this.weight = weight;
}

public Integer getBirth_year() {
    return birth_year;
}

public void setBirth_year(Integer birth_year) {
    this.birth_year = birth_year;
}

public Integer getAge() {
    return age;
}

public void setAge(Integer age) {
    this.age = age;
}

}
