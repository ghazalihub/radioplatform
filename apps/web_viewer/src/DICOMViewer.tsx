import React, { useEffect, useRef, useState } from 'react';
import { RenderingEngine, Enums, type Types, volumeLoader, cache } from '@cornerstonejs/core';
import * as cornerstoneTools from '@cornerstonejs/tools';
import { initCornerstone } from './cornerstoneInit';

const {
  WindowLevelTool,
  PanTool,
  ZoomTool,
  LengthTool,
  StackScrollTool,
  RectangleScissorsTool,
  SphereScissorsTool,
  CircleScissorsTool,
  PaintFillTool,
  BrushTool,
  ToolGroupManager,
  segmentation,
  Enums: csToolsEnums,
} = cornerstoneTools;

const DICOMViewer: React.FC<{ imageIds: string[] }> = ({ imageIds }) => {
  const elementRef = useRef<HTMLDivElement>(null);
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    const setup = async () => {
      await initCornerstone();
      setInitialized(true);
    };
    setup();
  }, []);

  useEffect(() => {
    if (!initialized || !elementRef.current || imageIds.length === 0) return;

    const renderingEngineId = 'myRenderingEngine';
    const viewportId = 'CT_AXIAL';
    const toolGroupId = 'myToolGroup';
    const volumeId = 'myVolume';

    const renderingEngine = new RenderingEngine(renderingEngineId);

    const viewportInputArray: any[] = [
      {
        viewportId,
        element: elementRef.current,
        type: Enums.ViewportType.ORTHOGRAPHIC,
        defaultOptions: {
          orientation: Enums.OrientationAxis.AXIAL,
        },
      },
    ];

    renderingEngine.setViewports(viewportInputArray);

    // Tools Setup
    cornerstoneTools.addTool(WindowLevelTool);
    cornerstoneTools.addTool(PanTool);
    cornerstoneTools.addTool(ZoomTool);
    cornerstoneTools.addTool(LengthTool);
    cornerstoneTools.addTool(StackScrollTool);
    cornerstoneTools.addTool(BrushTool);
    cornerstoneTools.addTool(RectangleScissorsTool);

    const toolGroup = ToolGroupManager.createToolGroup(toolGroupId);
    if (toolGroup) {
      toolGroup.addTool(WindowLevelTool.toolName);
      toolGroup.addTool(PanTool.toolName);
      toolGroup.addTool(ZoomTool.toolName);
      toolGroup.addTool(LengthTool.toolName);
      toolGroup.addTool(StackScrollTool.toolName);
      toolGroup.addTool(BrushTool.toolName);
      toolGroup.addTool(RectangleScissorsTool.toolName);

      toolGroup.addViewport(viewportId, renderingEngineId);

      toolGroup.setToolActive(WindowLevelTool.toolName, {
        bindings: [{ mouseButton: csToolsEnums.MouseBindings.Primary }],
      });
      toolGroup.setToolActive(PanTool.toolName, {
        bindings: [{ mouseButton: csToolsEnums.MouseBindings.Auxiliary }],
      });
      toolGroup.setToolActive(ZoomTool.toolName, {
        bindings: [{ mouseButton: csToolsEnums.MouseBindings.Secondary }],
      });
      toolGroup.setToolActive(StackScrollTool.toolName);
    }

    const setupVolume = async () => {
      // For MPR, we need to create a volume from the stack of images
      const volume = await volumeLoader.createAndCacheVolume(volumeId, { imageIds });
      volume.load();
      const viewport = renderingEngine.getViewport(viewportId) as Types.IVolumeViewport;
      viewport.setVolumes([{ volumeId }]);
      viewport.render();
    };
    setupVolume();

    // Initial segmentation setup
    const segmentationId = 'MY_SEGMENTATION';
    segmentation.addSegmentations([
      {
        segmentationId,
        representation: {
          type: csToolsEnums.SegmentationRepresentations.Labelmap,
          data: {
            volumeId: segmentationId,
          },
        },
      },
    ]);


    return () => {
      renderingEngine.destroy();
      ToolGroupManager.destroyToolGroup(toolGroupId);
    };
  }, [initialized, imageIds]);

  return (
    <div
      ref={elementRef}
      style={{ width: '500px', height: '500px', backgroundColor: 'black' }}
    />
  );
};

export default DICOMViewer;
