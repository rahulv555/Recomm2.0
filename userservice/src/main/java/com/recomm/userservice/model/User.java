package com.recomm.userservice.model;

import java.util.List;
import jakarta.persistence.Column;
import jakarta.persistence.CollectionTable;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Entity;
import jakarta.validation.constraints.NotNull;
import jakarta.persistence.Table;
import jakarta.persistence.Id;

@Entity
@Table(name = "user_profiles")
public class User {


    @Id
    @Column(updatable = false, nullable = false)
    private String userID; //will be auth token for new users

    @NotNull
    @Column
    private String name;

    @NotNull
    @Column
    private String smoker;

    @NotNull
    @Column 
    private String drink_Level;

    @NotNull
    @Column
    private String budget;

    @NotNull
    @Column
    private String dress_preference;

    @NotNull
    @Column
    private String ambience;

    @NotNull
    @Column
    private String transport;

    @NotNull
    @Column
    private String marital_status;

    @NotNull
    @Column
    private String hijos;

    @NotNull
    @Column
    private String personality;

    @NotNull
    @Column
    private String religion;

    @NotNull
    @Column
    private String interest;

    @NotNull
    @Column
    private String activity;

    @NotNull
    @Column
    private String color;

    @Column
    private String[] rcuisine;

    @NotNull
    @Column
    private Double height;

    @NotNull
    @Column
    private Double weight;

    @NotNull
    @Column
    private Integer birth_year;

    @NotNull
    @Column
    private Integer age;

    //  
    public String getUserID() {
    return userID;
}

public void setUserID(String userID) {
    this.userID = userID;
}
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

public String getDrink_Level() {
    return drink_Level;
}

public void setDrink_Level(String drink_Level) {
    this.drink_Level = drink_Level;
}

public String getBudget() {
    return budget;
}

public void setBudget(String budget) {
    this.budget = budget;
}

public String getDress_Preference() {
    return dress_preference;
}

public void setDress_Preference(String dress_preference) {
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

public String getMarital_Status() {
    return marital_status;
}

public void setMarital_Status(String marital_status) {
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
    return rcuisine;
}

public void setCuisine(String[] rcuisine) {
    this.rcuisine = rcuisine;
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
