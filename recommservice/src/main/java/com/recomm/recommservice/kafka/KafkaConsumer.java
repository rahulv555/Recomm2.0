package com.recomm.recommservice.kafka;


import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.protobuf.InvalidProtocolBufferException;
import com.recomm.recommservice.service.RecommService;

import user.events.CreateEvent;
import user.events.UpdateEvent;
import user.events.RateEvent;
import com.recomm.recommservice.service.RecommService;


@Service
public class KafkaConsumer {
    private static final Logger log = LoggerFactory.getLogger(KafkaConsumer.class);
    private final RecommService recommService;

    public KafkaConsumer(RecommService recommService) {
        this.recommService = recommService;
    }

    //connecting kafka consumer to kafka topic
    @KafkaListener(topics="user_created", groupId = "recomm-service")
    public void consumeCreateEvent(byte[] event){
        try {
            CreateEvent createEvent = CreateEvent.parseFrom(event);//CreateEvent from the code generated using proto
            //parseFrom will try to convert the byte array to a patientevent object

            
            //BUSINESS LOGIC HERE
            recommService.notifyUserUpdate(createEvent.getUserId());

            log.info("Received Create Event: [UserId={}]", createEvent.getUserId());

            
        } catch (InvalidProtocolBufferException e) {
            log.error("Error deserializing event {}", e.getMessage());
            e.printStackTrace();
        }
    }


    //connecting kafka consumer to kafka topic
    @KafkaListener(topics="user_updated", groupId = "recomm-service")
    public void consumeUpdateEvent(byte[] event){
        try {
            UpdateEvent updateEvent = UpdateEvent.parseFrom(event);//UpdateEvent from the code generated using proto
            //parseFrom will try to convert the byte array to a patientevent object


            //BUSINESS LOGIC HERE
            recommService.notifyUserUpdate(updateEvent.getUserId());

            log.info("Received Update Event: [UserId={}]", updateEvent.getUserId());

            
        } catch (InvalidProtocolBufferException e) {
            log.error("Error deserializing event {}", e.getMessage());
            e.printStackTrace();
        }
    }


    //connecting kafka consumer to kafka topic
    @KafkaListener(topics="rating", groupId = "recomm-service")
    public void consumeRatingEvent(byte[] event){
        try {
            RateEvent ratingEvent = RateEvent.parseFrom(event);//RatingEvent from the code generated using proto
            //parseFrom will try to convert the byte array to a patientevent object


            //BUSINESS LOGIC HERE
            recommService.notifyInteraction();
            

            log.info("Received Update Event: [UserId={}] [PlaceId={}] [rating={}] [Foodrating={}] [Servicerating={}]", ratingEvent.getUserId(), ratingEvent.getPlaceId(), ratingEvent.getRating(), ratingEvent.getFoodRating(), ratingEvent.getServiceRating());

            
        } catch (InvalidProtocolBufferException e) {
            log.error("Error deserializing event {}", e.getMessage());
            e.printStackTrace();
        }
    }
}
