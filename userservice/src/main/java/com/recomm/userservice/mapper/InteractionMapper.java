package com.recomm.userservice.mapper;

import com.recomm.userservice.dto.RatePlaceDTO;

import com.recomm.userservice.model.Interaction;

public class InteractionMapper {


       //Convert RatePlaceDTO to Interaction model
  public static Interaction toInteraction(RatePlaceDTO dto, String userID){
   Interaction inter = new Interaction();

    inter.setFoodRating(dto.getFoodRating());
    inter.setServiceRating(dto.getServiceRating());
    inter.setRating(dto.getRating());
    inter.setPlaceID(dto.getPlaceID());
    inter.setUserID(userID);
    

    return inter;

}


}