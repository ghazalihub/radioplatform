import * as cornerstone from '@cornerstonejs/core';
import { init as csRenderInit, imageLoader } from '@cornerstonejs/core';
import { init as csToolsInit } from '@cornerstonejs/tools';
import cornerstoneDICOMImageLoader from '@cornerstonejs/dicom-image-loader';
import dicomParser from 'dicom-parser';

export async function initCornerstone() {
  await csRenderInit();
  await csToolsInit();

  cornerstoneDICOMImageLoader.init();

  // Register image loader
  imageLoader.registerImageLoader('wado-rs', cornerstoneDICOMImageLoader.wadouri.loadImage);

  cornerstoneDICOMImageLoader.internal.setOptions({
    beforeSend: function (xhr: XMLHttpRequest) {
      // Add custom headers here (e.g. Auth tokens)
    },
  });
}
