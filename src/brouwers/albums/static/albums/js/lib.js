import $ from 'jquery';
import Q from 'q';
import Handlebars from 'handlebars';


export function bootstrap() {

    debugger;
    // $(function() {
    //     'use strict';

    //     // http://www.bootply.com/79859

    //     var $lightbox = $('#modal-lightbox'),
    //         $lightboxBody = $lightbox.find('.modal-content');


    //     $('#photo-thumbs').on('click', '.album-photo', function(event) {
    //         event.preventDefault();

    //         var id = $(this).data('id');

    //         // remove all 'old' bits
    //         $lightboxBody.find('.modal-body').remove();
    //         $('#image-loader').show();

    //         var renderLightbox = function(currentID, photos) {
    //             var current = photos.filter(function(e) {return e.id == currentID;})[0];
    //             current.state = {selected: true};
    //             var context = {
    //                 photos: photos,
    //                 current: current,
    //             };
    //             Handlebars
    //                 .render('albums::photo-lightbox', context)
    //                 .done(function(html) {
    //                     $lightboxBody.append(html);
    //                     $lightbox.find('.active img').on('load', function() {
    //                         $('#image-loader').hide();
    //                     });
    //                 });
    //         };

    //         /* Closure to render the current photo in the lightbox */
    //         function getLightboxRenderer(id) {
    //             var currentID = id;
    //             return function(photos) {
    //                 renderLightbox(currentID, photos);
    //                 $lightbox.find('.carousel').trigger('slide.bs.carousel');
    //             };
    //         }

    //         // bring up the modal with spinner
    //         $lightbox.modal('show');

    //         // fetch the photo details from the Api
    //         Photo.objects.filter({
    //             page: window.page,
    //             album: window.album
    //         }).done(getLightboxRenderer(id));

    //     });

    // });

}
