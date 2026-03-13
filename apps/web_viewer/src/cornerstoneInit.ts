import { init as csRenderInit } from '@cornerstonejs/core';
import { init as csToolsInit } from '@cornerstonejs/tools';
import cornerstoneDICOMImageLoader from '@cornerstonejs/dicom-image-loader';

export async function initCornerstone() {
  await csRenderInit();
  await csToolsInit();

  cornerstoneDICOMImageLoader.external.cornerstone = require('@cornerstonejs/core');
  cornerstoneDICOMImageLoader.external.dicomParser = require('dicom-parser');

  cornerstoneDICOMImageLoader.configure({
    beforeSend: function (xhr: XMLHttpRequest) {
      // Add custom headers here (e.g. Auth tokens)
    },
  });
}
