import React, { useEffect, useRef, useState } from 'react';
import { RenderingEngine, Enums, type Types } from '@cornerstonejs/core';
import * as cornerstoneTools from '@cornerstonejs/tools';
import { initCornerstone } from './cornerstoneInit';

const {
  WindowLevelTool,
  PanTool,
  ZoomTool,
  LengthTool,
  ToolGroupManager,
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
    const viewportIdSagittal = 'CT_SAGITTAL';
    const viewportIdCoronal = 'CT_CORONAL';
    const toolGroupId = 'myToolGroup';

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
      // In a real MPR viewer, you would have separate div elements for Sagittal and Coronal
    ];

    renderingEngine.setViewports(viewportInputArray);

    // Tools Setup
    cornerstoneTools.addTool(WindowLevelTool);
    cornerstoneTools.addTool(PanTool);
    cornerstoneTools.addTool(ZoomTool);
    cornerstoneTools.addTool(LengthTool);

    const toolGroup = ToolGroupManager.createToolGroup(toolGroupId);
    if (toolGroup) {
      toolGroup.addTool(WindowLevelTool.toolName);
      toolGroup.addTool(PanTool.toolName);
      toolGroup.addTool(ZoomTool.toolName);
      toolGroup.addTool(LengthTool.toolName);

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
    }

    const viewport = renderingEngine.getViewport(viewportId) as Types.IStackViewport;
    viewport.setStack(imageIds);
    viewport.render();

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
